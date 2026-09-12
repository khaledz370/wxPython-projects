//! Audio conversion (ffmpeg) and cover art (lofty, no re-encoding).

use crate::config::{self, Settings};
use crate::files::{self, TempFile};
use crate::images;
use crate::jobs::{parse_opts, run_files, FileResult, JobCtx, Outcome, Summary};
use crate::process::{self, Stream};
use lofty::config::WriteOptions;
use lofty::picture::{MimeType, Picture, PictureType};
use lofty::prelude::*;
use lofty::tag::Tag;
use serde::Deserialize;
use serde_json::Value;
use std::collections::VecDeque;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Deserialize)]
#[serde(default, rename_all = "camelCase")]
struct AudioOpts {
    convert: bool,
    format: String,
    /// kbps, 0 = encoder default / VBR
    bitrate: u32,
    sample_rate: u32,
    channels: u32,
    output: String,
    subfolder: String,
    folder: String,
    /// "keep" | "set" | "auto" | "remove" | "extract"
    cover: String,
    cover_path: String,
    cover_max: u32,
    threads: usize,
}

impl Default for AudioOpts {
    fn default() -> Self {
        Self {
            convert: true,
            format: "mp3".into(),
            bitrate: 0,
            sample_rate: 0,
            channels: 0,
            output: "subfolder".into(),
            subfolder: "converted".into(),
            folder: String::new(),
            cover: "keep".into(),
            cover_path: String::new(),
            cover_max: 1200,
            threads: 2,
        }
    }
}

/// (file extension, ffmpeg codec arguments)
fn codec_args(format: &str, bitrate: u32) -> Result<(&'static str, Vec<String>), String> {
    let rate = |default: u32| format!("{}k", if bitrate == 0 { default } else { bitrate });
    let args: (&str, Vec<&str>) = match format {
        "mp3" if bitrate == 0 => ("mp3", vec!["-c:a", "libmp3lame", "-q:a", "0"]),
        "mp3" => ("mp3", vec!["-c:a", "libmp3lame", "-b:a"]),
        "m4a" => ("m4a", vec!["-c:a", "aac", "-movflags", "+faststart", "-b:a"]),
        "opus" => ("opus", vec!["-c:a", "libopus", "-b:a"]),
        "ogg" if bitrate == 0 => ("ogg", vec!["-c:a", "libvorbis", "-q:a", "6"]),
        "ogg" => ("ogg", vec!["-c:a", "libvorbis", "-b:a"]),
        "flac" => ("flac", vec!["-c:a", "flac", "-compression_level", "8"]),
        "wav" => ("wav", vec!["-c:a", "pcm_s16le"]),
        "alac" => ("m4a", vec!["-c:a", "alac"]),
        other => return Err(format!("unknown audio format {other}")),
    };
    let mut list: Vec<String> = args.1.into_iter().map(String::from).collect();
    if list.last().map(String::as_str) == Some("-b:a") {
        let default = match format {
            "m4a" => 256,
            "opus" => 160,
            "ogg" => 224,
            _ => 256,
        };
        list.push(rate(default));
    }
    Ok((args.0, list))
}

enum CoverAction {
    Set(Vec<u8>, &'static str),
    Remove,
}

pub fn job(ctx: &JobCtx, s: &Settings, list: &[PathBuf], opts: Value) -> Result<Summary, String> {
    let o: AudioOpts = parse_opts(opts)?;
    let ffmpeg = if o.convert {
        Some(config::ffmpeg_exe(s).ok_or("ffmpeg not found. Install it or set its path in Settings.")?)
    } else {
        None
    };
    if !o.convert && o.cover == "keep" {
        return Err("Nothing to do: turn on conversion or pick a cover action".into());
    }
    if o.convert {
        codec_args(&o.format, o.bitrate)?;
    }
    let fixed_cover = if o.cover == "set" {
        if o.cover_path.trim().is_empty() {
            return Err("Choose the cover image".into());
        }
        Some(images::cover_bytes(Path::new(o.cover_path.trim()), o.cover_max)?)
    } else {
        None
    };
    let threads = o.threads.clamp(1, 16);
    Ok(run_files(ctx, list, threads, |i, f| {
        audio_one(ctx, &o, ffmpeg.as_deref(), fixed_cover.as_ref(), i, f)
    }))
}

fn audio_one(
    ctx: &JobCtx,
    o: &AudioOpts,
    ffmpeg: Option<&Path>,
    fixed_cover: Option<&(Vec<u8>, &'static str)>,
    index: usize,
    file: &Path,
) -> FileResult {
    if o.cover == "extract" && ffmpeg.is_none() {
        return extract_cover(file);
    }
    let source_cover = read_cover(file);

    let (target, converted) = match ffmpeg {
        Some(ff) => (convert(ctx, ff, o, index, file)?, true),
        None => (file.to_path_buf(), false),
    };

    let mut notes = Vec::new();
    let action = match o.cover.as_str() {
        "set" => fixed_cover.map(|(b, m)| CoverAction::Set(b.clone(), m)),
        "auto" => match find_folder_cover(file) {
            Some(img) => {
                let (bytes, mime) = images::cover_bytes(&img, o.cover_max)?;
                notes.push(format!("cover: {}", files::name_of(&img)));
                Some(CoverAction::Set(bytes, mime))
            }
            None => {
                notes.push("no cover image found in folder".into());
                source_cover.filter(|_| converted).map(|(b, m)| CoverAction::Set(b, m))
            }
        },
        "remove" => Some(CoverAction::Remove),
        "extract" => {
            if let Ok(Outcome::Done(m)) = extract_cover(file) {
                notes.push(m);
            }
            source_cover.filter(|_| converted).map(|(b, m)| CoverAction::Set(b, m))
        }
        _ => source_cover.filter(|_| converted).map(|(b, m)| CoverAction::Set(b, m)),
    };

    if let Some(action) = action {
        // converted files are new, the originals are edited through a temp copy
        if let Err(e) = apply_cover(&target, &action, !converted) {
            if !converted {
                return Err(e);
            }
            notes.push(format!("cover not embedded ({e})"));
        } else if o.cover != "keep" {
            notes.push(match action {
                CoverAction::Set(..) => "cover embedded".into(),
                CoverAction::Remove => "covers removed".into(),
            });
        }
    }

    let mut msg = if converted { format!("→ {}", files::name_of(&target)) } else { String::new() };
    for n in notes {
        if !msg.is_empty() {
            msg += " · ";
        }
        msg += &n;
    }
    Ok(Outcome::Done(msg))
}

fn parse_duration(line: &str) -> Option<f64> {
    let rest = line.trim_start().strip_prefix("Duration: ")?;
    let stamp = rest.split(',').next()?.trim();
    let mut parts = stamp.split(':');
    let h: f64 = parts.next()?.parse().ok()?;
    let m: f64 = parts.next()?.parse().ok()?;
    let s: f64 = parts.next()?.parse().ok()?;
    Some(h * 3600.0 + m * 60.0 + s)
}

fn convert(ctx: &JobCtx, ffmpeg: &Path, o: &AudioOpts, index: usize, file: &Path) -> Result<PathBuf, String> {
    let (ext, codec) = codec_args(&o.format, o.bitrate)?;
    let dir = files::output_dir(file, &o.output, &o.subfolder, &o.folder)?;
    let target = files::unique_path(&dir.join(format!("{}.{ext}", files::stem_of(file))));
    let tmp = TempFile::new(files::temp_sibling(&target));

    let mut cmd = process::command(ffmpeg);
    cmd.args(["-hide_banner", "-nostdin", "-y", "-i"]).arg(file);
    cmd.args(["-map", "0:a:0", "-vn", "-sn", "-dn", "-map_metadata", "0"]);
    cmd.args(&codec);
    if o.sample_rate > 0 {
        cmd.args(["-ar", &o.sample_rate.to_string()]);
    }
    if o.channels > 0 {
        cmd.args(["-ac", &o.channels.to_string()]);
    }
    cmd.args(["-progress", "pipe:1", "-nostats"]).arg(tmp.path());

    let mut duration = 0.0;
    let mut last_errors: VecDeque<String> = VecDeque::new();
    let code = process::run(ctx, cmd, |stream, line| match stream {
        Stream::Err => {
            if duration == 0.0 {
                if let Some(d) = parse_duration(line) {
                    duration = d;
                }
            }
            last_errors.push_back(line.trim().to_string());
            if last_errors.len() > 3 {
                last_errors.pop_front();
            }
        }
        Stream::Out => {
            let value = line.strip_prefix("out_time_us=").or_else(|| line.strip_prefix("out_time_ms="));
            if let Some(us) = value.and_then(|v| v.trim().parse::<f64>().ok()) {
                if duration > 0.0 {
                    ctx.progress(index, (us / 1e6 / duration * 95.0) as f32);
                }
            }
        }
    })?;
    if code != 0 {
        let detail: Vec<String> = last_errors.into_iter().collect();
        return Err(format!("ffmpeg failed: {}", detail.join(" | ")));
    }
    files::move_file(tmp.path(), &target).map_err(|e| format!("Can't save output: {e}"))?;
    Ok(target)
}

fn read_cover(file: &Path) -> Option<(Vec<u8>, &'static str)> {
    let tagged = lofty::read_from_path(file).ok()?;
    let pictures: Vec<&Picture> = tagged.tags().iter().flat_map(|t| t.pictures()).collect();
    let pic = pictures
        .iter()
        .find(|p| p.pic_type() == PictureType::CoverFront)
        .or(pictures.first())?;
    let mime = if pic.mime_type() == Some(&MimeType::Png) { "image/png" } else { "image/jpeg" };
    Some((pic.data().to_vec(), mime))
}

fn apply_cover(path: &Path, action: &CoverAction, via_copy: bool) -> Result<(), String> {
    let copy = if via_copy {
        let tmp = TempFile::new(files::temp_sibling(path));
        fs::copy(path, tmp.path()).map_err(|e| format!("Can't copy file: {e}"))?;
        Some(tmp)
    } else {
        None
    };
    let work = copy.as_ref().map(|t| t.path()).unwrap_or(path);

    let mut tagged = lofty::read_from_path(work).map_err(|e| format!("tags: {e}"))?;
    if tagged.primary_tag().is_none() {
        let tag_type = tagged.primary_tag_type();
        tagged.insert_tag(Tag::new(tag_type));
    }
    let tag = tagged.primary_tag_mut().ok_or("this format has no tag support")?;
    let types: Vec<PictureType> = tag.pictures().iter().map(|p| p.pic_type()).collect();
    for t in types {
        tag.remove_picture_type(t);
    }
    if let CoverAction::Set(bytes, mime) = action {
        let mime = if *mime == "image/png" { MimeType::Png } else { MimeType::Jpeg };
        tag.push_picture(Picture::new_unchecked(PictureType::CoverFront, Some(mime), None, bytes.clone()));
    }
    tag.save_to_path(work, WriteOptions::default()).map_err(|e| format!("tags: {e}"))?;

    if let Some(tmp) = &copy {
        files::move_file(tmp.path(), path).map_err(|e| format!("Can't replace file: {e}"))?;
    }
    Ok(())
}

fn extract_cover(file: &Path) -> FileResult {
    let Some((bytes, mime)) = read_cover(file) else {
        return Ok(Outcome::Skipped("no embedded cover".into()));
    };
    let ext = if mime == "image/png" { "png" } else { "jpg" };
    let dir = file.parent().unwrap_or(Path::new("."));
    let out = files::unique_path(&dir.join(format!("{}.cover.{ext}", files::stem_of(file))));
    files::write_atomic(&out, &bytes)?;
    Ok(Outcome::Done(format!("cover saved as {}", files::name_of(&out))))
}

/// `Song.jpg` next to `Song.mp3`, else cover/folder/front/album art of the folder.
fn find_folder_cover(file: &Path) -> Option<PathBuf> {
    let dir = file.parent()?;
    let stem = files::stem_of(file).to_lowercase();
    let images: Vec<PathBuf> = fs::read_dir(dir)
        .ok()?
        .flatten()
        .map(|e| e.path())
        .filter(|p| ["jpg", "jpeg", "png", "webp"].contains(&files::ext_of(p).as_str()))
        .collect();
    let named = |name: &str| images.iter().find(|p| files::stem_of(p).to_lowercase() == name).cloned();
    named(&stem).or_else(|| ["cover", "folder", "front", "album", "albumart"].iter().find_map(|n| named(n)))
}

pub fn cover_preview(file: &Path) -> Option<String> {
    let (bytes, _) = read_cover(file)?;
    images::bytes_thumbnail(&bytes, 320).ok()
}
