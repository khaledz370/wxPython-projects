//! MKVToolNix powered jobs: remux, in-place property edits, extraction,
//! adding sidecar subtitles/audio, crop and custom mkvmerge presets.

use crate::config::{self, Settings};
use crate::files::{self, Finalized, TempFile};
use crate::images;
use crate::jobs::{parse_opts, run_files, FileResult, JobCtx, Outcome, Summary};
use crate::langs;
use crate::process;
use crate::subtitles;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashSet;
use std::ffi::{OsStr, OsString};
use std::fs;
use std::path::{Path, PathBuf};

pub const MATROSKA_EXTS: &[&str] = &["mkv", "mka", "mks", "mk3d", "webm"];
pub const SUB_EXTS: &[&str] = &["srt", "ass", "ssa", "vtt", "sup", "idx", "sub", "usf"];
pub const AUDIO_SIDECAR_EXTS: &[&str] = &[
    "mka", "aac", "ac3", "eac3", "dts", "flac", "mp3", "opus", "ogg", "m4a", "wav", "thd",
];
const TEXT_SUB_EXTS: &[&str] = &["srt", "ass", "ssa", "vtt"];

pub fn is_matroska(p: &Path) -> bool {
    MATROSKA_EXTS.contains(&files::ext_of(p).as_str())
}

pub struct Tools {
    pub mkvmerge: PathBuf,
    pub mkvpropedit: PathBuf,
    pub mkvextract: PathBuf,
}

pub fn tools(s: &Settings) -> Result<Tools, String> {
    let find = |name: &str| {
        config::mkvtoolnix_exe(s, name).ok_or_else(|| {
            format!("{name}.exe not found. Install MKVToolNix or set its folder in Settings.")
        })
    };
    Ok(Tools {
        mkvmerge: find("mkvmerge")?,
        mkvpropedit: find("mkvpropedit")?,
        mkvextract: find("mkvextract")?,
    })
}

// ---------------------------------------------------------------------------
// Identification (mkvmerge -J)
// ---------------------------------------------------------------------------

#[derive(Serialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct Track {
    pub id: i64,
    /// "video" | "audio" | "subtitles"
    pub kind: String,
    /// 1-based position among tracks of the same kind (mkvpropedit "a2" style selectors)
    pub index: usize,
    pub selector: String,
    pub codec: String,
    pub codec_id: String,
    pub language: String,
    pub name: String,
    pub default: bool,
    pub forced: bool,
    pub enabled: bool,
    pub dims: String,
    pub channels: i64,
    pub sample_rate: i64,
}

#[derive(Serialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct Attachment {
    pub id: i64,
    pub uid: String,
    pub name: String,
    pub mime: String,
    pub size: u64,
}

#[derive(Serialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct MkvInfo {
    pub container: String,
    pub title: String,
    pub duration_ms: u64,
    pub tracks: Vec<Track>,
    pub attachments: Vec<Attachment>,
    pub chapters: usize,
}

impl MkvInfo {
    pub fn of_kind(&self, kind: &str) -> Vec<&Track> {
        self.tracks.iter().filter(|t| t.kind == kind).collect()
    }
}

pub fn identify(mkvmerge: &Path, file: &Path) -> Result<MkvInfo, String> {
    let out = process::command(mkvmerge)
        .arg("-J")
        .arg(file)
        .output()
        .map_err(|e| format!("Could not run mkvmerge: {e}"))?;
    let v: Value = serde_json::from_slice(&out.stdout)
        .map_err(|_| "mkvmerge returned no identification data".to_string())?;
    if let Some(errors) = v["errors"].as_array().filter(|e| !e.is_empty()) {
        let text: Vec<&str> = errors.iter().filter_map(Value::as_str).collect();
        return Err(text.join("; "));
    }
    if v["container"]["recognized"].as_bool() == Some(false)
        || v["container"]["supported"].as_bool() == Some(false)
    {
        return Err("file format not recognized by mkvmerge".into());
    }

    let props = &v["container"]["properties"];
    let mut counts = std::collections::HashMap::new();
    let mut tracks = Vec::new();
    for t in v["tracks"].as_array().into_iter().flatten() {
        let kind = t["type"].as_str().unwrap_or("").to_string();
        let letter = match kind.as_str() {
            "video" => "v",
            "audio" => "a",
            "subtitles" => "s",
            _ => "x",
        };
        let n = counts.entry(letter).or_insert(0usize);
        *n += 1;
        let p = &t["properties"];
        let language = [&p["language_ietf"], &p["language"]]
            .iter()
            .filter_map(|v| v.as_str())
            .find(|s| !s.is_empty())
            .unwrap_or("und")
            .to_string();
        tracks.push(Track {
            id: t["id"].as_i64().unwrap_or(0),
            index: *n,
            selector: format!("{letter}{n}"),
            codec: t["codec"].as_str().unwrap_or("").to_string(),
            codec_id: p["codec_id"].as_str().unwrap_or("").to_string(),
            language,
            name: p["track_name"].as_str().unwrap_or("").to_string(),
            default: p["default_track"].as_bool().unwrap_or(false),
            forced: p["forced_track"].as_bool().unwrap_or(false),
            enabled: p["enabled_track"].as_bool().unwrap_or(true),
            dims: p["pixel_dimensions"].as_str().unwrap_or("").to_string(),
            channels: p["audio_channels"].as_i64().unwrap_or(0),
            sample_rate: p["audio_sampling_frequency"].as_i64().unwrap_or(0),
            kind,
        });
    }

    let attachments = v["attachments"]
        .as_array()
        .into_iter()
        .flatten()
        .map(|a| Attachment {
            id: a["id"].as_i64().unwrap_or(0),
            uid: a["properties"]["uid"].to_string(),
            name: a["file_name"].as_str().unwrap_or("").to_string(),
            mime: a["content_type"].as_str().unwrap_or("").to_string(),
            size: a["size"].as_u64().unwrap_or(0),
        })
        .collect();

    let chapters = v["chapters"]
        .as_array()
        .into_iter()
        .flatten()
        .map(|c| c["num_entries"].as_u64().unwrap_or(0) as usize)
        .sum();

    Ok(MkvInfo {
        container: v["container"]["type"].as_str().unwrap_or("").to_string(),
        title: props["title"].as_str().unwrap_or("").to_string(),
        duration_ms: props["duration"].as_u64().unwrap_or(0) / 1_000_000,
        tracks,
        attachments,
        chapters,
    })
}

// ---------------------------------------------------------------------------
// Running the tools
// ---------------------------------------------------------------------------

/// Argument list that always starts with English messages + machine readable progress.
struct Args(Vec<OsString>);

impl Args {
    fn new() -> Self {
        Self(vec!["--ui-language".into(), "en".into(), "--gui-mode".into()])
    }
    fn add(&mut self, arg: impl AsRef<OsStr>) -> &mut Self {
        self.0.push(arg.as_ref().to_os_string());
        self
    }
}

fn parse_progress(line: &str) -> Option<f32> {
    let rest = line
        .strip_prefix("#GUI#progress ")
        .or_else(|| line.strip_prefix("Progress: "))?;
    rest.trim().trim_end_matches('%').parse().ok()
}

fn strip_any(line: &str, prefixes: &[&str]) -> Option<String> {
    prefixes
        .iter()
        .find_map(|p| line.strip_prefix(p))
        .map(|rest| rest.trim().to_string())
}

/// Runs mkvmerge / mkvextract / mkvpropedit, mapping its progress into `range`.
/// Exit code 1 means "finished with warnings" and counts as success. Returns the warnings.
pub fn run_tool(
    ctx: &JobCtx,
    index: usize,
    exe: &Path,
    args: &[OsString],
    range: (f32, f32),
) -> Result<Vec<String>, String> {
    let mut cmd = process::command(exe);
    cmd.args(args);
    let mut warnings = Vec::new();
    let mut errors = Vec::new();
    let code = process::run(ctx, cmd, |_, line| {
        if let Some(p) = parse_progress(line) {
            ctx.progress(index, range.0 + (range.1 - range.0) * p / 100.0);
        } else if let Some(w) = strip_any(line, &["#GUI#warning", "Warning:"]) {
            warnings.push(w);
        } else if let Some(e) = strip_any(line, &["#GUI#error", "Error:"]) {
            errors.push(e);
        }
    })?;
    let tool = files::stem_of(exe);
    for w in &warnings {
        ctx.log("warn", &format!("{tool}: {w}"));
    }
    if !(0..=1).contains(&code) {
        return Err(errors
            .last()
            .cloned()
            .unwrap_or_else(|| format!("{tool} exited with code {code}")));
    }
    Ok(warnings)
}

fn outcome(fin: Finalized, warnings: &[String]) -> Outcome {
    let mut msg = format!("→ {}", files::name_of(&fin.path));
    if !fin.note.is_empty() {
        msg += &format!(" · {}", fin.note);
    }
    if !warnings.is_empty() {
        msg += &format!(" · {} warning(s)", warnings.len());
    }
    if fin.warning || !warnings.is_empty() {
        Outcome::Warn(msg)
    } else {
        Outcome::Done(msg)
    }
}

fn title_value(mode: &str, custom: &str, file: &Path) -> Option<String> {
    match mode {
        "filename" => Some(files::stem_of(file)),
        "clear" => Some(String::new()),
        "custom" => Some(custom.to_string()),
        _ => None,
    }
}

fn select_by_lang(tracks: &[&Track], spec: &str) -> Option<Vec<i64>> {
    let wanted = langs::tokens(spec);
    if wanted.is_empty() {
        return None;
    }
    Some(
        tracks
            .iter()
            .filter(|t| wanted.iter().any(|w| langs::matches(&t.language, w)))
            .map(|t| t.id)
            .collect(),
    )
}

fn join_ids(ids: &[i64]) -> String {
    ids.iter().map(i64::to_string).collect::<Vec<_>>().join(",")
}

/// spec: "" = leave flags alone, "none" = no default track, otherwise a language.
fn default_flags(args: &mut Args, tracks: &[&Track], spec: &str) {
    let spec = spec.trim();
    if spec.is_empty() {
        return;
    }
    let chosen = if spec == "none" {
        None
    } else {
        match tracks.iter().find(|t| langs::matches(&t.language, spec)) {
            Some(t) => Some(t.id),
            None => return,
        }
    };
    for t in tracks {
        let flag = if Some(t.id) == chosen { "yes" } else { "no" };
        args.add("--default-track-flag").add(format!("{}:{flag}", t.id));
    }
}

fn mkv_target(file: &Path) -> PathBuf {
    file.with_file_name(format!("{}.mkv", files::stem_of(file)))
}

// ---------------------------------------------------------------------------
// Remux
// ---------------------------------------------------------------------------

#[derive(Deserialize, Default)]
#[serde(default, rename_all = "camelCase")]
struct RemuxOpts {
    audio_langs: String,
    subtitle_langs: String,
    default_audio: String,
    default_subtitle: String,
    no_attachments: bool,
    no_chapters: bool,
    no_global_tags: bool,
    title_mode: String,
    title: String,
    chapter_minutes: u32,
}

pub fn remux(ctx: &JobCtx, s: &Settings, list: &[PathBuf], opts: Value) -> Result<Summary, String> {
    let o: RemuxOpts = parse_opts(opts)?;
    let t = tools(s)?;
    Ok(run_files(ctx, list, s.parallel_files.clamp(1, 16), |i, f| remux_one(ctx, s, &t, &o, i, f)))
}

fn remux_one(ctx: &JobCtx, s: &Settings, t: &Tools, o: &RemuxOpts, index: usize, file: &Path) -> FileResult {
    let (input, backup_note) = if s.original_policy.moves_to_backup() {
        files::backup_original(s, file)?
    } else {
        (file.to_path_buf(), String::new())
    };
    let info = identify(&t.mkvmerge, &input)?;
    let out = mkv_target(file);
    let tmp = TempFile::new(files::temp_sibling(&out));

    let mut a = Args::new();
    a.add("-o").add(tmp.path());
    if let Some(title) = title_value(&o.title_mode, &o.title, file) {
        a.add("--title").add(title);
    }
    if o.chapter_minutes > 0 {
        let m = o.chapter_minutes;
        a.add("--generate-chapters").add(format!("interval:{:02}:{:02}:00", m / 60, m % 60));
    }

    let audio = info.of_kind("audio");
    let subs = info.of_kind("subtitles");
    let kept_audio: Vec<&Track> = match select_by_lang(&audio, &o.audio_langs) {
        Some(ids) if ids.is_empty() && !audio.is_empty() => {
            return Ok(Outcome::Skipped(format!(
                "no audio track matches \"{}\", left untouched instead of making it silent",
                o.audio_langs.trim()
            )))
        }
        Some(ids) => {
            if !ids.is_empty() {
                a.add("--audio-tracks").add(join_ids(&ids));
            }
            audio.iter().copied().filter(|t| ids.contains(&t.id)).collect()
        }
        None => audio.clone(),
    };
    let kept_subs: Vec<&Track> = match select_by_lang(&subs, &o.subtitle_langs) {
        Some(ids) if ids.is_empty() => {
            a.add("--no-subtitles");
            Vec::new()
        }
        Some(ids) => {
            a.add("--subtitle-tracks").add(join_ids(&ids));
            subs.iter().copied().filter(|t| ids.contains(&t.id)).collect()
        }
        None => subs.clone(),
    };
    default_flags(&mut a, &kept_audio, &o.default_audio);
    default_flags(&mut a, &kept_subs, &o.default_subtitle);
    if o.no_attachments {
        a.add("--no-attachments");
    }
    if o.no_chapters || o.chapter_minutes > 0 {
        a.add("--no-chapters");
    }
    if o.no_global_tags {
        a.add("--no-global-tags");
    }
    a.add(&input);

    files::check_space(&out, files::size_of(&input))?;
    let warnings = run_tool(ctx, index, &t.mkvmerge, &a.0, (0.0, 100.0))?;
    if !backup_note.is_empty() {
        files::move_file(tmp.path(), &out).map_err(|e| format!("Can't save output: {e}"))?;
        return Ok(outcome(
            Finalized { path: out, note: backup_note, warning: false },
            &warnings,
        ));
    }
    let fin = files::finalize(s, file, tmp.path(), &out)?;
    Ok(outcome(fin, &warnings))
}

// ---------------------------------------------------------------------------
// Extract (mkvextract)
// ---------------------------------------------------------------------------

#[derive(Deserialize)]
#[serde(default, rename_all = "camelCase")]
struct ExtractOpts {
    video: bool,
    audio: bool,
    subtitles: bool,
    attachments: bool,
    chapters: bool,
    langs: String,
    audio_as_mka: bool,
    out_dir: String,
    /// true: every file lands in one shared folder, false: one `<name>_extracted` folder per file.
    single_folder: bool,
}

impl Default for ExtractOpts {
    fn default() -> Self {
        Self {
            video: false,
            audio: true,
            subtitles: true,
            attachments: false,
            chapters: false,
            langs: String::new(),
            audio_as_mka: false,
            out_dir: String::new(),
            single_folder: true,
        }
    }
}

const CODEC_EXTS: &[(&str, &str)] = &[
    ("V_MPEG4/ISO/AVC", "h264"),
    ("V_MPEGH/ISO/HEVC", "h265"),
    ("V_AV1", "ivf"),
    ("V_VP8", "ivf"),
    ("V_VP9", "ivf"),
    ("V_MPEG1", "mpg"),
    ("V_MPEG2", "mpg"),
    ("V_MS/VFW", "avi"),
    ("A_AAC", "aac"),
    ("A_AC3", "ac3"),
    ("A_EAC3", "eac3"),
    ("A_DTS", "dts"),
    ("A_FLAC", "flac"),
    ("A_OPUS", "opus"),
    ("A_VORBIS", "ogg"),
    ("A_MPEG/L3", "mp3"),
    ("A_MPEG/L2", "mp2"),
    ("A_TRUEHD", "thd"),
    ("A_MLP", "mlp"),
    ("A_PCM", "wav"),
    ("A_ALAC", "caf"),
    ("A_TTA1", "tta"),
    ("A_WAVPACK4", "wv"),
    ("S_TEXT/UTF8", "srt"),
    ("S_TEXT/ASCII", "srt"),
    ("S_TEXT/ASS", "ass"),
    ("S_TEXT/SSA", "ssa"),
    ("S_TEXT/WEBVTT", "vtt"),
    ("S_TEXT/USF", "usf"),
    ("S_HDMV/PGS", "sup"),
    ("S_VOBSUB", "sub"),
    ("S_KATE", "ogg"),
];

fn codec_ext(codec_id: &str) -> &'static str {
    let c = codec_id.to_ascii_uppercase();
    CODEC_EXTS
        .iter()
        .find(|(prefix, _)| c.starts_with(prefix))
        .map(|(_, ext)| *ext)
        .unwrap_or("bin")
}

pub fn extract(ctx: &JobCtx, s: &Settings, list: &[PathBuf], opts: Value) -> Result<Summary, String> {
    let o: ExtractOpts = parse_opts(opts)?;
    let t = tools(s)?;
    Ok(run_files(ctx, list, s.parallel_files.clamp(1, 16), |i, f| extract_one(ctx, &t, &o, i, f)))
}

fn extract_one(ctx: &JobCtx, t: &Tools, o: &ExtractOpts, index: usize, file: &Path) -> FileResult {
    if !is_matroska(file) {
        return Ok(Outcome::Skipped("mkvextract only reads Matroska/WebM, remux it to MKV first".into()));
    }
    let info = identify(&t.mkvmerge, file)?;
    let stem = files::stem_of(file);
    let base = if o.out_dir.trim().is_empty() {
        file.parent().unwrap_or(Path::new(".")).to_path_buf()
    } else {
        PathBuf::from(o.out_dir.trim())
    };
    let out_dir = match (o.single_folder, o.out_dir.trim().is_empty()) {
        (true, true) => base.join("extracted"),
        (true, false) => base,
        (false, true) => base.join(format!("{stem}_extracted")),
        (false, false) => base.join(files::sanitize(&stem)),
    };
    let wanted = langs::tokens(&o.langs);
    let lang_ok = |t: &Track| wanted.is_empty() || wanted.iter().any(|w| langs::matches(&t.language, w));

    let mut track_specs = Vec::new();
    let mut mka_ids = Vec::new();
    for tr in &info.tracks {
        let want = match tr.kind.as_str() {
            "video" => o.video,
            "audio" => o.audio && lang_ok(tr),
            "subtitles" => o.subtitles && lang_ok(tr),
            _ => false,
        };
        if !want {
            continue;
        }
        if tr.kind == "audio" && o.audio_as_mka {
            mka_ids.push(tr.id);
            continue;
        }
        let label = match tr.kind.as_str() {
            "video" => "video",
            "audio" => "audio",
            _ => "sub",
        };
        let mut name = format!("{stem}.{label}{}", tr.index);
        if !tr.language.is_empty() && tr.language != "und" {
            name += &format!(".{}", tr.language);
        }
        if tr.forced {
            name += ".forced";
        }
        name += &format!(".{}", codec_ext(&tr.codec_id));
        let dest = files::unique_path(&out_dir.join(files::sanitize(&name)));
        track_specs.push(format!("{}:{}", tr.id, dest.display()));
    }

    let mut attachment_specs = Vec::new();
    if o.attachments {
        let mut used = HashSet::new();
        for at in &info.attachments {
            // Shared folder: prefix with the file stem so parallel files can't clobber each other.
            let att_name = if o.single_folder { format!("{stem}.{}", at.name) } else { at.name.clone() };
            let mut dest = files::unique_path(&out_dir.join(files::sanitize(&att_name)));
            if !used.insert(dest.clone()) {
                dest = out_dir.join(format!("{}-{}", at.id, files::sanitize(&att_name)));
            }
            attachment_specs.push(format!("{}:{}", at.id, dest.display()));
        }
    }
    let chapters = o.chapters && info.chapters > 0;
    let extract_any = !track_specs.is_empty() || !attachment_specs.is_empty() || chapters;
    if !extract_any && mka_ids.is_empty() {
        return Ok(Outcome::Skipped("nothing matches the selected track types / languages".into()));
    }
    fs::create_dir_all(&out_dir).map_err(|e| format!("Can't create {}: {e}", out_dir.display()))?;

    let mut warnings = Vec::new();
    let mut count = 0;
    let split = match (extract_any, mka_ids.is_empty()) {
        (true, true) => 100.0,
        (false, _) => 0.0,
        (true, false) => 50.0,
    };
    if extract_any {
        let mut a = Args::new();
        a.add(file);
        if !track_specs.is_empty() {
            a.add("tracks");
            for spec in &track_specs {
                a.add(spec);
            }
        }
        if !attachment_specs.is_empty() {
            a.add("attachments");
            for spec in &attachment_specs {
                a.add(spec);
            }
        }
        if chapters {
            a.add("chapters").add(files::unique_path(&out_dir.join(format!("{stem}.chapters.xml"))));
        }
        warnings.extend(run_tool(ctx, index, &t.mkvextract, &a.0, (0.0, split))?);
        count += track_specs.len() + attachment_specs.len() + chapters as usize;
    }
    if !mka_ids.is_empty() {
        let dest = files::unique_path(&out_dir.join(format!("{stem}.audio.mka")));
        let mut a = Args::new();
        a.add("-o").add(&dest);
        a.add("--no-video").add("--no-subtitles").add("--no-attachments");
        a.add("--audio-tracks").add(join_ids(&mka_ids)).add(file);
        warnings.extend(run_tool(ctx, index, &t.mkvmerge, &a.0, (split, 100.0))?);
        count += 1;
    }
    let msg = format!("{count} item(s) → {}", files::name_of(&out_dir));
    Ok(if warnings.is_empty() { Outcome::Done(msg) } else { Outcome::Warn(msg) })
}

// ---------------------------------------------------------------------------
// Add sidecar subtitles / audio
// ---------------------------------------------------------------------------

#[derive(Serialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct Sidecar {
    pub path: String,
    pub file: String,
    pub kind: String,
    pub lang: String,
    pub forced: bool,
    pub sdh: bool,
    pub name: String,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct MuxPreview {
    pub video: String,
    pub sidecars: Vec<Sidecar>,
}

/// Finds files named like the video: `Movie.srt`, `Movie.ar.srt`, `Movie.eng.forced.ass`, `Movie.en.sdh.srt`...
pub fn find_sidecars(video: &Path, subs: bool, audio: bool, default_lang: &str) -> Vec<Sidecar> {
    let Some(dir) = video.parent() else { return Vec::new() };
    let stem = files::stem_of(video);
    let stem_lower = stem.to_lowercase();
    let mut entries: Vec<PathBuf> = fs::read_dir(dir)
        .map(|rd| rd.flatten().map(|e| e.path()).filter(|p| p.is_file()).collect())
        .unwrap_or_default();
    entries.sort_by(|a, b| files::natural_cmp(&a.to_string_lossy(), &b.to_string_lossy()));
    let lower_names: HashSet<String> = entries.iter().map(|p| files::name_of(p).to_lowercase()).collect();

    let mut found = Vec::new();
    for p in entries {
        if files::same_file(&p, video) {
            continue;
        }
        let fname = files::name_of(&p);
        let prefix_ok = fname
            .get(..stem.len())
            .map(|s| s.to_lowercase() == stem_lower)
            .unwrap_or(false);
        let rest = fname.get(stem.len()..).unwrap_or("");
        if !prefix_ok || !rest.starts_with('.') {
            continue;
        }
        let ext = files::ext_of(&p);
        let kind = if subs && SUB_EXTS.contains(&ext.as_str()) {
            "subtitles"
        } else if audio && AUDIO_SIDECAR_EXTS.contains(&ext.as_str()) {
            "audio"
        } else {
            continue;
        };
        let lower = fname.to_lowercase();
        if ext == "sub" && lower_names.contains(&format!("{}idx", &lower[..lower.len() - 3])) {
            continue; // VobSub: mkvmerge reads the .idx, which pulls in the .sub
        }
        let middle = rest[1..rest.len().saturating_sub(ext.len())].trim_matches('.');
        let (mut lang, mut forced, mut sdh, mut name_parts) = (String::new(), false, false, Vec::new());
        for token in middle.split('.').filter(|t| !t.is_empty()) {
            let lower = token.to_lowercase();
            if lower == "forced" || lower == "force" {
                forced = true;
            } else if ["sdh", "cc", "hi"].contains(&lower.as_str()) {
                sdh = true;
            } else if lower == "default" {
            } else if let (true, Some(l)) = (lang.is_empty(), langs::find(token)) {
                lang = l.0.to_string();
            } else {
                name_parts.push(token.to_string());
            }
        }
        if lang.is_empty() {
            lang = if default_lang.trim().is_empty() { "und".into() } else { default_lang.trim().into() };
        }
        found.push(Sidecar {
            path: p.to_string_lossy().into_owned(),
            file: fname.clone(),
            kind: kind.into(),
            lang,
            forced,
            sdh,
            name: name_parts.join(" "),
        });
    }
    found
}

#[derive(Deserialize)]
#[serde(default, rename_all = "camelCase")]
struct MuxOpts {
    subtitles: bool,
    audio: bool,
    default_lang: String,
    make_default: bool,
    remove_existing_subs: bool,
    dispose_sidecars: bool,
}

impl Default for MuxOpts {
    fn default() -> Self {
        Self {
            subtitles: true,
            audio: false,
            default_lang: "und".into(),
            make_default: true,
            remove_existing_subs: false,
            dispose_sidecars: false,
        }
    }
}

pub fn mux(ctx: &JobCtx, s: &Settings, list: &[PathBuf], opts: Value) -> Result<Summary, String> {
    let o: MuxOpts = parse_opts(opts)?;
    let t = tools(s)?;
    Ok(run_files(ctx, list, s.parallel_files.clamp(1, 16), |i, f| mux_one(ctx, s, &t, &o, i, f)))
}

fn mux_one(ctx: &JobCtx, s: &Settings, t: &Tools, o: &MuxOpts, index: usize, file: &Path) -> FileResult {
    let sidecars = find_sidecars(file, o.subtitles, o.audio, &o.default_lang);
    if sidecars.is_empty() {
        return Ok(Outcome::Skipped("no matching subtitle / audio files next to it".into()));
    }
    let info = identify(&t.mkvmerge, file)?;
    let out = mkv_target(file);
    let tmp = TempFile::new(files::temp_sibling(&out));

    let mut a = Args::new();
    a.add("-o").add(tmp.path());
    let adds_subs = sidecars.iter().any(|c| c.kind == "subtitles");
    if o.remove_existing_subs && adds_subs {
        a.add("--no-subtitles");
    } else if o.make_default && adds_subs {
        for tr in info.of_kind("subtitles") {
            a.add("--default-track-flag").add(format!("{}:no", tr.id));
        }
    }
    a.add(file);

    let mut first_sub = true;
    for car in &sidecars {
        a.add("--language").add(format!("0:{}", car.lang));
        if !car.name.is_empty() {
            a.add("--track-name").add(format!("0:{}", car.name));
        }
        if car.forced {
            a.add("--forced-display-flag").add("0:yes");
        }
        if car.sdh {
            a.add("--hearing-impaired-flag").add("0:yes");
        }
        let is_default = car.kind == "subtitles" && o.make_default && first_sub;
        a.add("--default-track-flag").add(if is_default { "0:yes" } else { "0:no" });
        if car.kind == "subtitles" {
            first_sub = false;
            let ext = files::ext_of(Path::new(&car.path));
            if TEXT_SUB_EXTS.contains(&ext.as_str()) {
                let bytes = fs::read(&car.path).map_err(|e| format!("{}: {e}", car.file))?;
                if let Some(charset) = subtitles::detect_charset(&bytes) {
                    a.add("--sub-charset").add(format!("0:{charset}"));
                }
            }
        }
        a.add(&car.path);
    }

    files::check_space(&out, files::size_of(file))?;
    let warnings = run_tool(ctx, index, &t.mkvmerge, &a.0, (0.0, 100.0))?;
    let fin = files::finalize(s, file, tmp.path(), &out)?;
    let mut result = outcome(fin, &warnings);
    if o.dispose_sidecars {
        for car in &sidecars {
            if let Err(e) = files::dispose_original(s, Path::new(&car.path)) {
                ctx.log("warn", &format!("{}: {e}", car.file));
            }
        }
    }
    let added = format!("+{} track(s) ", sidecars.len());
    match &mut result {
        Outcome::Done(m) | Outcome::Warn(m) | Outcome::Skipped(m) => m.insert_str(0, &added),
    }
    Ok(result)
}

// ---------------------------------------------------------------------------
// Crop
// ---------------------------------------------------------------------------

#[derive(Deserialize, Default)]
#[serde(default, rename_all = "camelCase")]
struct CropOpts {
    top: u32,
    right: u32,
    bottom: u32,
    left: u32,
    clear: bool,
}

pub fn crop(ctx: &JobCtx, s: &Settings, list: &[PathBuf], opts: Value) -> Result<Summary, String> {
    let o: CropOpts = parse_opts(opts)?;
    if !o.clear && o.top + o.right + o.bottom + o.left == 0 {
        return Err("All crop values are 0. Enter values or choose \"Remove crop\".".into());
    }
    let t = tools(s)?;
    Ok(run_files(ctx, list, s.parallel_files.clamp(1, 16), |i, f| crop_one(ctx, s, &t, &o, i, f)))
}

fn parse_dims(dims: &str) -> Option<(u32, u32)> {
    let (w, h) = dims.split_once('x')?;
    Some((w.trim().parse().ok()?, h.trim().parse().ok()?))
}

fn crop_one(ctx: &JobCtx, s: &Settings, t: &Tools, o: &CropOpts, index: usize, file: &Path) -> FileResult {
    let info = identify(&t.mkvmerge, file)?;
    let Some(video) = info.of_kind("video").first().map(|v| (*v).clone()) else {
        return Ok(Outcome::Skipped("no video track".into()));
    };
    if !o.clear {
        if let Some((w, h)) = parse_dims(&video.dims) {
            if o.left + o.right >= w || o.top + o.bottom >= h {
                return Err(format!("crop is larger than the picture ({w}×{h})"));
            }
        }
    }

    if is_matroska(file) {
        let mut a = Args::new();
        a.add(file).add("--edit").add("track:v1");
        if o.clear {
            for side in ["top", "left", "right", "bottom"] {
                a.add("--delete").add(format!("pixel-crop-{side}"));
            }
        } else {
            for (side, v) in [("top", o.top), ("left", o.left), ("right", o.right), ("bottom", o.bottom)] {
                a.add("--set").add(format!("pixel-crop-{side}={v}"));
            }
        }
        let warnings = run_tool(ctx, index, &t.mkvpropedit, &a.0, (0.0, 100.0))?;
        let msg = if o.clear {
            "crop removed (edited in place)".to_string()
        } else {
            format!("crop T{} R{} B{} L{} set (edited in place)", o.top, o.right, o.bottom, o.left)
        };
        return Ok(if warnings.is_empty() { Outcome::Done(msg) } else { Outcome::Warn(msg) });
    }

    if o.clear {
        return Ok(Outcome::Skipped("not a Matroska file, there is no crop to remove".into()));
    }
    let out = mkv_target(file);
    let tmp = TempFile::new(files::temp_sibling(&out));
    let mut a = Args::new();
    a.add("-o").add(tmp.path());
    a.add("--cropping").add(format!("{}:{},{},{},{}", video.id, o.left, o.top, o.right, o.bottom));
    a.add(file);
    files::check_space(&out, files::size_of(file))?;
    let warnings = run_tool(ctx, index, &t.mkvmerge, &a.0, (0.0, 100.0))?;
    let fin = files::finalize(s, file, tmp.path(), &out)?;
    Ok(outcome(fin, &warnings))
}

// ---------------------------------------------------------------------------
// Track & property editor (mkvpropedit, in place)
// ---------------------------------------------------------------------------

#[derive(Deserialize, Default)]
#[serde(default, rename_all = "camelCase")]
struct TrackEdit {
    selector: String,
    language: Option<String>,
    name: Option<String>,
    default: Option<bool>,
    forced: Option<bool>,
    enabled: Option<bool>,
}

#[derive(Deserialize, Default)]
#[serde(default, rename_all = "camelCase")]
struct PropsOpts {
    title_mode: String,
    title: String,
    edits: Vec<TrackEdit>,
    delete_attachments: bool,
    delete_chapters: bool,
    delete_tags: bool,
    cover: String,
}

struct Cover {
    path: PathBuf,
    name: String,
    mime: String,
}

pub fn props(ctx: &JobCtx, s: &Settings, list: &[PathBuf], opts: Value) -> Result<Summary, String> {
    let o: PropsOpts = parse_opts(opts)?;
    let t = tools(s)?;
    let cover = if o.cover.trim().is_empty() {
        None
    } else {
        let (bytes, mime) = images::cover_bytes(Path::new(o.cover.trim()), 0)?;
        let ext = if mime == "image/png" { "png" } else { "jpg" };
        let path = ctx.temp_dir()?.join(format!("cover.{ext}"));
        fs::write(&path, bytes).map_err(|e| format!("Cover: {e}"))?;
        Some(Cover { path, name: format!("cover.{ext}"), mime: mime.to_string() })
    };
    Ok(run_files(ctx, list, s.parallel_files.clamp(1, 16), |i, f| props_one(ctx, &t, &o, cover.as_ref(), i, f)))
}

fn parse_selector(sel: &str) -> Option<(&'static str, usize)> {
    let kind = match sel.chars().next()? {
        'v' => "video",
        'a' => "audio",
        's' => "subtitles",
        _ => return None,
    };
    let n: usize = sel[1..].parse().ok()?;
    (n > 0).then_some((kind, n))
}

fn props_one(ctx: &JobCtx, t: &Tools, o: &PropsOpts, cover: Option<&Cover>, index: usize, file: &Path) -> FileResult {
    if !is_matroska(file) {
        return Ok(Outcome::Skipped("mkvpropedit only edits Matroska files, remux it first".into()));
    }
    let info = identify(&t.mkvmerge, file)?;
    let mut a = Args::new();
    a.add(file);
    let mut changes = 0;
    let mut notes = Vec::new();

    if let Some(title) = title_value(&o.title_mode, &o.title, file) {
        a.add("--edit").add("info");
        if title.is_empty() {
            a.add("--delete").add("title");
        } else {
            a.add("--set").add(format!("title={title}"));
        }
        changes += 1;
    }

    for e in &o.edits {
        let Some((kind, n)) = parse_selector(&e.selector) else { continue };
        if info.of_kind(kind).len() < n {
            notes.push(format!("no track {}", e.selector));
            continue;
        }
        let mut ops: Vec<String> = Vec::new();
        if let Some(lang) = e.language.as_deref().filter(|l| !l.trim().is_empty()) {
            ops.extend(["--set".into(), format!("language={}", lang.trim())]);
        }
        if let Some(name) = &e.name {
            if name.is_empty() {
                ops.extend(["--delete".into(), "name".into()]);
            } else {
                ops.extend(["--set".into(), format!("name={name}")]);
            }
        }
        for (flag, value) in [("flag-default", e.default), ("flag-forced", e.forced), ("flag-enabled", e.enabled)] {
            if let Some(v) = value {
                ops.extend(["--set".into(), format!("{flag}={}", v as u8)]);
            }
        }
        if ops.is_empty() {
            continue;
        }
        a.add("--edit").add(format!("track:{}", e.selector));
        for op in ops {
            a.add(op);
        }
        changes += 1;
    }

    if o.delete_chapters && info.chapters > 0 {
        a.add("--chapters").add("");
        changes += 1;
    }
    if o.delete_tags {
        a.add("--tags").add("all:");
        changes += 1;
    }
    if o.delete_attachments {
        for at in &info.attachments {
            a.add("--delete-attachment").add(format!("={}", at.uid));
            changes += 1;
        }
    }
    if let Some(c) = cover {
        if !o.delete_attachments {
            for at in info.attachments.iter().filter(|at| at.name.to_lowercase().starts_with("cover")) {
                a.add("--delete-attachment").add(format!("={}", at.uid));
            }
        }
        a.add("--attachment-name").add(&c.name);
        a.add("--attachment-mime-type").add(&c.mime);
        a.add("--add-attachment").add(&c.path);
        changes += 1;
    }

    if changes == 0 {
        let why = if notes.is_empty() { "no changes to apply".to_string() } else { notes.join(", ") };
        return Ok(Outcome::Skipped(why));
    }
    let warnings = run_tool(ctx, index, &t.mkvpropedit, &a.0, (0.0, 100.0))?;
    let mut msg = format!("{changes} change(s) written in place");
    if !notes.is_empty() {
        msg += &format!(" · {}", notes.join(", "));
    }
    Ok(if warnings.is_empty() && notes.is_empty() { Outcome::Done(msg) } else { Outcome::Warn(msg) })
}

// ---------------------------------------------------------------------------
// Custom mkvmerge preset (MKVToolNix GUI option file or typed arguments)
// ---------------------------------------------------------------------------

#[derive(Deserialize, Default)]
#[serde(default, rename_all = "camelCase")]
struct PresetOpts {
    source: String,
    options_file: String,
    args: String,
}

/// Reads an option file saved by MKVToolNix GUI ("Multiplexer → Create option file")
/// and removes everything that belongs to the original job (output name, input file).
pub fn parse_options_file(path: &Path) -> Result<Vec<String>, String> {
    let text = fs::read_to_string(path).map_err(|e| format!("Can't read option file: {e}"))?;
    let raw: Vec<String> = serde_json::from_str(text.trim_start_matches('\u{feff}'))
        .map_err(|_| "Not an MKVToolNix option file (expected a JSON array of arguments)".to_string())?;
    clean_args(raw)
}

fn clean_args(raw: Vec<String>) -> Result<Vec<String>, String> {
    let inputs = raw.iter().filter(|a| a.as_str() == "(").count();
    if inputs > 1 {
        return Err(format!(
            "the option file uses {inputs} input files; only single-input option files can be applied to a batch"
        ));
    }
    let mut out = Vec::new();
    let mut it = raw.into_iter();
    let mut in_group = false;
    while let Some(arg) = it.next() {
        if in_group {
            in_group = arg != ")";
            continue;
        }
        match arg.as_str() {
            "(" => in_group = true,
            "-o" | "--output" | "--ui-language" => {
                it.next();
            }
            "--gui-mode" => {}
            _ => out.push(arg),
        }
    }
    Ok(out)
}

pub fn preset_args(source: &str, options_file: &str, args: &str) -> Result<Vec<String>, String> {
    if source == "args" {
        let parsed = shell_words::split(args).map_err(|e| format!("Arguments: {e}"))?;
        clean_args(parsed)
    } else {
        if options_file.trim().is_empty() {
            return Err("Choose an MKVToolNix option file".into());
        }
        parse_options_file(Path::new(options_file.trim()))
    }
}

pub fn preset(ctx: &JobCtx, s: &Settings, list: &[PathBuf], opts: Value) -> Result<Summary, String> {
    let o: PresetOpts = parse_opts(opts)?;
    let args = preset_args(&o.source, &o.options_file, &o.args)?;
    if args.is_empty() {
        return Err("The preset has no options".into());
    }
    let t = tools(s)?;
    Ok(run_files(ctx, list, s.parallel_files.clamp(1, 16), |i, file| {
        let out = mkv_target(file);
        let tmp = TempFile::new(files::temp_sibling(&out));
        let mut a = Args::new();
        a.add("-o").add(tmp.path());
        for arg in &args {
            a.add(arg);
        }
        a.add(file);
        files::check_space(&out, files::size_of(file))?;
        let warnings = run_tool(ctx, i, &t.mkvmerge, &a.0, (0.0, 100.0))?;
        let fin = files::finalize(s, file, tmp.path(), &out)?;
        Ok(outcome(fin, &warnings))
    }))
}
