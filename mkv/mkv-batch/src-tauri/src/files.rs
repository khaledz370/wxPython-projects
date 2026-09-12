//! File helpers: scanning, safe output names, temp files and what happens to originals.
//!
//! Safety rules used everywhere in the app:
//! * new files are written to a temp name next to the target and only renamed when complete;
//! * an existing file is never overwritten unless the user asked for it;
//! * a source file is only moved (backup folder / Recycle Bin) after its replacement succeeded.

use crate::config::{OriginalPolicy, Settings};
use serde::Serialize;
use std::cmp::Ordering;
use std::collections::HashSet;
use std::fs;
use std::io;
use std::path::{Component, Path, PathBuf};

pub const TEMP_MARKER: &str = ".mkvbatch-tmp.";

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct FileEntry {
    pub path: String,
    pub name: String,
    pub dir: String,
    pub size: u64,
    pub ext: String,
}

pub fn ext_of(p: &Path) -> String {
    p.extension()
        .map(|e| e.to_string_lossy().to_lowercase())
        .unwrap_or_default()
}

pub fn stem_of(p: &Path) -> String {
    p.file_stem()
        .map(|s| s.to_string_lossy().into_owned())
        .unwrap_or_default()
}

pub fn name_of(p: &Path) -> String {
    p.file_name()
        .map(|s| s.to_string_lossy().into_owned())
        .unwrap_or_default()
}

pub fn size_of(p: &Path) -> u64 {
    fs::metadata(p).map(|m| m.len()).unwrap_or(0)
}

/// Expands files and folders into a sorted, de-duplicated list filtered by extension.
pub fn scan(paths: &[String], exts: &[String], recursive: bool) -> Vec<FileEntry> {
    let exts: Vec<String> = exts
        .iter()
        .map(|e| e.trim_start_matches('.').to_lowercase())
        .collect();
    let mut out = Vec::new();
    let mut seen = HashSet::new();
    for p in paths {
        let p = PathBuf::from(p);
        if p.is_dir() {
            walk(&p, recursive, &exts, &mut out, &mut seen);
        } else if p.is_file() {
            push_entry(&p, &exts, &mut out, &mut seen);
        }
    }
    out.sort_by(|a, b| natural_cmp(&a.path, &b.path));
    out
}

fn walk(dir: &Path, recursive: bool, exts: &[String], out: &mut Vec<FileEntry>, seen: &mut HashSet<String>) {
    let Ok(entries) = fs::read_dir(dir) else { return };
    for entry in entries.flatten() {
        let p = entry.path();
        if p.is_dir() {
            // never re-import our own backup folders
            if recursive && !name_of(&p).eq_ignore_ascii_case("_originals") {
                walk(&p, recursive, exts, out, seen);
            }
        } else {
            push_entry(&p, exts, out, seen);
        }
    }
}

fn push_entry(p: &Path, exts: &[String], out: &mut Vec<FileEntry>, seen: &mut HashSet<String>) {
    let name = name_of(p);
    if name.contains(TEMP_MARKER) {
        return;
    }
    let ext = ext_of(p);
    if !exts.is_empty() && !exts.contains(&ext) {
        return;
    }
    let key = p.to_string_lossy().to_lowercase();
    if !seen.insert(key) {
        return;
    }
    out.push(FileEntry {
        path: p.to_string_lossy().into_owned(),
        name,
        dir: p.parent().map(|d| d.to_string_lossy().into_owned()).unwrap_or_default(),
        size: size_of(p),
        ext,
    });
}

/// "Episode 2" sorts before "Episode 10".
pub fn natural_cmp(a: &str, b: &str) -> Ordering {
    let (mut a, mut b) = (a.chars().peekable(), b.chars().peekable());
    loop {
        match (a.peek().copied(), b.peek().copied()) {
            (None, None) => return Ordering::Equal,
            (None, Some(_)) => return Ordering::Less,
            (Some(_), None) => return Ordering::Greater,
            (Some(x), Some(y)) if x.is_ascii_digit() && y.is_ascii_digit() => {
                let mut na = String::new();
                while let Some(c) = a.peek().copied().filter(char::is_ascii_digit) {
                    na.push(c);
                    a.next();
                }
                let mut nb = String::new();
                while let Some(c) = b.peek().copied().filter(char::is_ascii_digit) {
                    nb.push(c);
                    b.next();
                }
                let (ta, tb) = (na.trim_start_matches('0'), nb.trim_start_matches('0'));
                let ord = ta.len().cmp(&tb.len()).then_with(|| ta.cmp(tb));
                if ord != Ordering::Equal {
                    return ord;
                }
            }
            (Some(x), Some(y)) => {
                let ord = x.to_lowercase().cmp(y.to_lowercase());
                if ord != Ordering::Equal {
                    return ord;
                }
                a.next();
                b.next();
            }
        }
    }
}

/// `name.ext` if free, otherwise `name (1).ext`, `name (2).ext`, ...
pub fn unique_path(p: &Path) -> PathBuf {
    if !p.exists() {
        return p.to_path_buf();
    }
    let dir = p.parent().unwrap_or(Path::new("."));
    let stem = stem_of(p);
    let ext = p.extension().map(|e| e.to_string_lossy().into_owned());
    (1..)
        .map(|i| match &ext {
            Some(e) => dir.join(format!("{stem} ({i}).{e}")),
            None => dir.join(format!("{stem} ({i})")),
        })
        .find(|c| !c.exists())
        .unwrap()
}

/// Temp file on the same volume as `target` (so the final rename is instant and atomic).
pub fn temp_sibling(target: &Path) -> PathBuf {
    let dir = target.parent().unwrap_or(Path::new("."));
    let name = match target.extension() {
        Some(ext) => format!("{}{TEMP_MARKER}{}", stem_of(target), ext.to_string_lossy()),
        None => format!("{}{TEMP_MARKER}tmp", stem_of(target)),
    };
    unique_path(&dir.join(name))
}

/// Deletes the file on drop unless it was moved away (e.g. on error or cancel).
pub struct TempFile(PathBuf);

impl TempFile {
    pub fn new(path: PathBuf) -> Self {
        Self(path)
    }
    pub fn path(&self) -> &Path {
        &self.0
    }
}

impl Drop for TempFile {
    fn drop(&mut self) {
        if self.0.exists() {
            let _ = fs::remove_file(&self.0);
        }
    }
}

/// Rename, falling back to copy + delete across drives.
pub fn move_file(src: &Path, dst: &Path) -> io::Result<()> {
    if fs::rename(src, dst).is_ok() {
        return Ok(());
    }
    if let Err(e) = fs::copy(src, dst) {
        let _ = fs::remove_file(dst);
        return Err(e);
    }
    fs::remove_file(src)
}

pub fn same_file(a: &Path, b: &Path) -> bool {
    match (fs::canonicalize(a), fs::canonicalize(b)) {
        (Ok(x), Ok(y)) => x == y,
        _ => a.to_string_lossy().to_lowercase() == b.to_string_lossy().to_lowercase(),
    }
}

pub fn backup_dir_for(s: &Settings, original: &Path) -> PathBuf {
    let name = s.backup_dir.trim();
    let name = if name.is_empty() { "mkv_old" } else { name };
    let p = Path::new(name);
    if p.is_absolute() {
        p.to_path_buf()
    } else if s.backup_same_dir {
        original.parent().unwrap_or(Path::new(".")).to_path_buf()
    } else {
        let mut root = PathBuf::new();
        for component in original.components() {
            root.push(component.as_os_str());
            if matches!(component, Component::RootDir) { break; }
        }
        if root.as_os_str().is_empty() { original.parent().unwrap_or(Path::new(".")).join(p) } else { root.join(p) }
    }
}

/// Moves a replaced source out of the way according to the user's policy.
pub fn dispose_original(s: &Settings, original: &Path) -> Result<String, String> {
    match s.original_policy {
        OriginalPolicy::Keep => Ok(String::new()),
        OriginalPolicy::Recycle => trash::delete(original)
            .map(|_| "original sent to Recycle Bin".to_string())
            .map_err(|e| format!("Recycle Bin: {e}")),
        OriginalPolicy::Backup => {
            let dir = backup_dir_for(s, original);
            fs::create_dir_all(&dir).map_err(|e| format!("Can't create {}: {e}", dir.display()))?;
            let dst = unique_path(&dir.join(name_of(original)));
            move_file(original, &dst).map_err(|e| format!("Can't move original: {e}"))?;
            Ok(format!("original moved to {}", name_of(&dir)))
        }
    }
}

pub struct Finalized {
    pub path: PathBuf,
    pub note: String,
    pub warning: bool,
}

/// Puts a finished temp output in place of `target` and deals with `original`.
pub fn finalize(s: &Settings, original: &Path, tmp: &Path, target: &Path) -> Result<Finalized, String> {
    let move_err = |e: io::Error| format!("Can't save output: {e}");

    if same_file(target, original) {
        if s.original_policy == OriginalPolicy::Keep {
            let dst = unique_path(target);
            move_file(tmp, &dst).map_err(move_err)?;
            return Ok(Finalized { path: dst, note: "original kept".into(), warning: false });
        }
        return match dispose_original(s, original) {
            Ok(note) => {
                move_file(tmp, target).map_err(move_err)?;
                Ok(Finalized { path: target.to_path_buf(), note, warning: false })
            }
            Err(e) => {
                // the original stays untouched; keep the new file next to it
                let dst = unique_path(target);
                move_file(tmp, &dst).map_err(move_err)?;
                Ok(Finalized { path: dst, note: format!("original left in place ({e})"), warning: true })
            }
        };
    }

    let dst = unique_path(target);
    move_file(tmp, &dst).map_err(move_err)?;
    match dispose_original(s, original) {
        Ok(note) => Ok(Finalized { path: dst, note, warning: false }),
        Err(e) => Ok(Finalized { path: dst, note: format!("original left in place ({e})"), warning: true }),
    }
}

/// Refuses to start when the target drive can't hold the output.
pub fn check_space(target: &Path, needed: u64) -> Result<(), String> {
    let dir = target.parent().unwrap_or(Path::new("."));
    match fs4::available_space(dir) {
        Ok(free) if free < needed + 64 * 1024 * 1024 => Err(format!(
            "not enough free space on {} (needs about {}, {} free)",
            dir.display(),
            human_size(needed),
            human_size(free)
        )),
        _ => Ok(()),
    }
}

/// Folder where converted media goes: next to the source, a subfolder, or a fixed folder.
pub fn output_dir(input: &Path, mode: &str, subfolder: &str, folder: &str) -> Result<PathBuf, String> {
    let parent = input.parent().unwrap_or(Path::new("."));
    let dir = match mode {
        "subfolder" => parent.join(if subfolder.trim().is_empty() { "converted" } else { subfolder.trim() }),
        "folder" => {
            if folder.trim().is_empty() {
                return Err("Choose an output folder".into());
            }
            PathBuf::from(folder.trim())
        }
        _ => parent.to_path_buf(),
    };
    fs::create_dir_all(&dir).map_err(|e| format!("Can't create {}: {e}", dir.display()))?;
    Ok(dir)
}

pub fn sanitize(name: &str) -> String {
    let cleaned: String = name
        .chars()
        .map(|c| if c.is_control() || r#"<>:"/\|?*"#.contains(c) { '_' } else { c })
        .collect();
    let cleaned = cleaned.trim().trim_end_matches('.').to_string();
    if cleaned.is_empty() { "file".into() } else { cleaned }
}

pub fn human_size(n: u64) -> String {
    let units = ["B", "KB", "MB", "GB", "TB"];
    let mut v = n as f64;
    let mut u = 0;
    while v >= 1024.0 && u < units.len() - 1 {
        v /= 1024.0;
        u += 1;
    }
    if u == 0 { format!("{n} B") } else { format!("{v:.1} {}", units[u]) }
}

pub fn write_atomic(target: &Path, bytes: &[u8]) -> Result<(), String> {
    let tmp = TempFile::new(temp_sibling(target));
    fs::write(tmp.path(), bytes).map_err(|e| format!("Can't write {}: {e}", target.display()))?;
    move_file(tmp.path(), target).map_err(|e| format!("Can't write {}: {e}", target.display()))
}

/// Opens Explorer with the file selected (or the folder itself).
pub fn reveal(path: &Path) {
    let mut cmd = std::process::Command::new("explorer");
    if path.is_dir() {
        cmd.arg(path);
    } else {
        #[cfg(windows)]
        {
            use std::os::windows::process::CommandExt;
            cmd.raw_arg(format!("/select,\"{}\"", path.display()));
        }
    }
    let _ = cmd.spawn();
}
