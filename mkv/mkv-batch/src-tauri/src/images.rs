//! Image conversion (pure Rust, multi-threaded): format, quality, resize, EXIF rotation.

use crate::config::Settings;
use crate::files;
use crate::jobs::{parse_opts, run_files, FileResult, JobCtx, Outcome, Summary};
use base64::Engine;
use image::codecs::ico::{IcoEncoder, IcoFrame};
use image::codecs::jpeg::JpegEncoder;
use image::codecs::png::{CompressionType, FilterType as PngFilter, PngEncoder};
use image::codecs::webp::WebPEncoder;
use image::imageops::FilterType;
use image::{
    DynamicImage, ExtendedColorType, GenericImageView, ImageDecoder, ImageFormat, ImageReader, Rgb,
    RgbImage, RgbaImage,
};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::io::Cursor;
use std::path::{Path, PathBuf};

pub const FORMATS: &[&str] = &["png", "jpg", "webp", "bmp", "gif", "tiff", "ico", "tga", "qoi"];

#[derive(Deserialize)]
#[serde(default, rename_all = "camelCase")]
struct ImageOpts {
    format: String,
    quality: u8,
    webp_lossless: bool,
    resize: String,
    max_width: u32,
    max_height: u32,
    percent: u32,
    background: String,
    output: String,
    subfolder: String,
    folder: String,
    overwrite: bool,
    auto_orient: bool,
    threads: usize,
}

impl Default for ImageOpts {
    fn default() -> Self {
        Self {
            format: "png".into(),
            quality: 85,
            webp_lossless: false,
            resize: "none".into(),
            max_width: 1920,
            max_height: 1920,
            percent: 50,
            background: "#ffffff".into(),
            output: "subfolder".into(),
            subfolder: "converted".into(),
            folder: String::new(),
            overwrite: false,
            auto_orient: true,
            threads: 0,
        }
    }
}

pub fn load(path: &Path, auto_orient: bool) -> Result<DynamicImage, String> {
    let mut reader = ImageReader::open(path)
        .map_err(|e| e.to_string())?
        .with_guessed_format()
        .map_err(|e| e.to_string())?;
    reader.no_limits();
    let mut decoder = reader.into_decoder().map_err(|e| format!("can't decode: {e}"))?;
    let orientation = if auto_orient { decoder.orientation().ok() } else { None };
    let mut img = DynamicImage::from_decoder(decoder).map_err(|e| format!("can't decode: {e}"))?;
    if let Some(o) = orientation {
        img.apply_orientation(o);
    }
    Ok(img)
}

fn parse_hex(color: &str) -> [u8; 3] {
    let hex = color.trim().trim_start_matches('#');
    let channel = |i: usize| hex.get(i..i + 2).and_then(|h| u8::from_str_radix(h, 16).ok()).unwrap_or(255);
    if hex.len() == 6 { [channel(0), channel(2), channel(4)] } else { [255, 255, 255] }
}

/// Removes transparency by blending onto `bg` (for formats without alpha, e.g. JPEG).
fn flatten(img: &DynamicImage, bg: [u8; 3]) -> RgbImage {
    if !img.color().has_alpha() {
        return img.to_rgb8();
    }
    let rgba = img.to_rgba8();
    let mut out = RgbImage::new(rgba.width(), rgba.height());
    for (x, y, p) in rgba.enumerate_pixels() {
        let a = p[3] as u32;
        let mix = |c: u8, b: u8| ((c as u32 * a + b as u32 * (255 - a)) / 255) as u8;
        out.put_pixel(x, y, Rgb([mix(p[0], bg[0]), mix(p[1], bg[1]), mix(p[2], bg[2])]));
    }
    out
}

fn to_8bit(img: &DynamicImage) -> DynamicImage {
    if img.color().has_alpha() {
        DynamicImage::ImageRgba8(img.to_rgba8())
    } else {
        DynamicImage::ImageRgb8(img.to_rgb8())
    }
}

fn resize(img: DynamicImage, o: &ImageOpts) -> DynamicImage {
    let (w, h) = img.dimensions();
    match o.resize.as_str() {
        "fit" => {
            let mw = if o.max_width == 0 { w } else { o.max_width.min(w) };
            let mh = if o.max_height == 0 { h } else { o.max_height.min(h) };
            if w <= mw && h <= mh { img } else { img.resize(mw, mh, FilterType::Lanczos3) }
        }
        "percent" if o.percent > 0 && o.percent != 100 => {
            let scale = |v: u32| ((v as u64 * o.percent as u64) / 100).max(1) as u32;
            img.resize_exact(scale(w), scale(h), FilterType::Lanczos3)
        }
        _ => img,
    }
}

fn ico_bytes(img: &DynamicImage) -> Result<Vec<u8>, String> {
    let (w, h) = img.dimensions();
    let side = w.max(h);
    let square = if w == h {
        img.to_rgba8()
    } else {
        let mut canvas = RgbaImage::new(side, side);
        image::imageops::overlay(&mut canvas, &img.to_rgba8(), ((side - w) / 2) as i64, ((side - h) / 2) as i64);
        canvas
    };
    let square = DynamicImage::ImageRgba8(square);
    let mut sizes: Vec<u32> = [256, 128, 64, 48, 32, 24, 16].into_iter().filter(|&s| s <= side).collect();
    if sizes.is_empty() {
        sizes.push(16);
    }
    let frames = sizes
        .iter()
        .map(|&s| {
            let px = square.resize_exact(s, s, FilterType::Lanczos3).to_rgba8();
            IcoFrame::as_png(px.as_raw(), s, s, ExtendedColorType::Rgba8)
        })
        .collect::<Result<Vec<_>, _>>()
        .map_err(|e| e.to_string())?;
    let mut buf = Vec::new();
    IcoEncoder::new(&mut buf).encode_images(&frames).map_err(|e| e.to_string())?;
    Ok(buf)
}

fn encode(img: &DynamicImage, format: &str, quality: u8, webp_lossless: bool, bg: [u8; 3]) -> Result<Vec<u8>, String> {
    let mut buf = Vec::new();
    let err = |e: image::ImageError| e.to_string();
    match format {
        "jpg" => {
            let rgb = DynamicImage::ImageRgb8(flatten(img, bg));
            rgb.write_with_encoder(JpegEncoder::new_with_quality(&mut buf, quality)).map_err(err)?;
        }
        "png" => {
            let enc = PngEncoder::new_with_quality(&mut buf, CompressionType::Best, PngFilter::Adaptive);
            img.write_with_encoder(enc).map_err(err)?;
        }
        "webp" if webp_lossless => {
            to_8bit(img).write_with_encoder(WebPEncoder::new_lossless(&mut buf)).map_err(err)?;
        }
        "webp" => {
            let rgba = img.to_rgba8();
            buf = webp::Encoder::from_rgba(rgba.as_raw(), rgba.width(), rgba.height())
                .encode(quality as f32)
                .to_vec();
        }
        "ico" => buf = ico_bytes(img)?,
        other => {
            let fmt = match other {
                "bmp" => ImageFormat::Bmp,
                "gif" => ImageFormat::Gif,
                "tiff" => ImageFormat::Tiff,
                "tga" => ImageFormat::Tga,
                "qoi" => ImageFormat::Qoi,
                _ => return Err(format!("unsupported output format {other}")),
            };
            let img = if fmt == ImageFormat::Gif { DynamicImage::ImageRgba8(img.to_rgba8()) } else { to_8bit(img) };
            img.write_to(&mut Cursor::new(&mut buf), fmt).map_err(err)?;
        }
    }
    Ok(buf)
}

pub fn convert(ctx: &JobCtx, _s: &Settings, list: &[PathBuf], opts: Value) -> Result<Summary, String> {
    let o: ImageOpts = parse_opts(opts)?;
    if !FORMATS.contains(&o.format.as_str()) {
        return Err(format!("Unknown output format {}", o.format));
    }
    if o.output == "folder" && o.folder.trim().is_empty() {
        return Err("Choose an output folder".into());
    }
    let bg = parse_hex(&o.background);
    let threads = if o.threads == 0 {
        std::thread::available_parallelism().map(|n| n.get()).unwrap_or(4)
    } else {
        o.threads
    };
    Ok(run_files(ctx, list, threads, |_, f| convert_one(&o, bg, f)))
}

fn convert_one(o: &ImageOpts, bg: [u8; 3], file: &Path) -> FileResult {
    let img = load(file, o.auto_orient)?;
    let (w0, h0) = img.dimensions();
    let img = resize(img, o);
    let (w, h) = img.dimensions();
    let bytes = encode(&img, &o.format, o.quality.clamp(1, 100), o.webp_lossless, bg)?;

    let dir = files::output_dir(file, &o.output, &o.subfolder, &o.folder)?;
    let target = dir.join(format!("{}.{}", files::stem_of(file), o.format));
    // the source itself is never overwritten
    let target = if o.overwrite && !files::same_file(&target, file) { target } else { files::unique_path(&target) };
    files::write_atomic(&target, &bytes)?;

    let size = if (w0, h0) == (w, h) { format!("{w}×{h}") } else { format!("{w0}×{h0} → {w}×{h}") };
    Ok(Outcome::Done(format!(
        "{size} · {} → {} · {}",
        files::human_size(files::size_of(file)),
        files::human_size(bytes.len() as u64),
        files::name_of(&target)
    )))
}

// --- previews and covers --------------------------------------------------------

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Thumb {
    pub data_url: String,
    pub width: u32,
    pub height: u32,
    pub format: String,
    pub size: u64,
}

fn data_url(img: &DynamicImage, max: u32) -> Result<String, String> {
    let small = img.thumbnail(max, max);
    let mut buf = Vec::new();
    let mime = if small.color().has_alpha() {
        small.write_to(&mut Cursor::new(&mut buf), ImageFormat::Png).map_err(|e| e.to_string())?;
        "image/png"
    } else {
        DynamicImage::ImageRgb8(small.to_rgb8())
            .write_with_encoder(JpegEncoder::new_with_quality(&mut buf, 82))
            .map_err(|e| e.to_string())?;
        "image/jpeg"
    };
    Ok(format!("data:{mime};base64,{}", base64::engine::general_purpose::STANDARD.encode(buf)))
}

pub fn thumbnail(path: &Path, max: u32) -> Result<Thumb, String> {
    let img = load(path, true)?;
    let (width, height) = img.dimensions();
    Ok(Thumb {
        data_url: data_url(&img, max)?,
        width,
        height,
        format: files::ext_of(path).to_uppercase(),
        size: files::size_of(path),
    })
}

pub fn bytes_thumbnail(bytes: &[u8], max: u32) -> Result<String, String> {
    let img = image::load_from_memory(bytes).map_err(|e| e.to_string())?;
    data_url(&img, max)
}

/// Image ready to embed as cover art: JPEG/PNG kept as-is when small enough,
/// anything else (WebP, BMP, huge images...) re-encoded as JPEG. `max` 0 = no resize.
pub fn cover_bytes(path: &Path, max: u32) -> Result<(Vec<u8>, &'static str), String> {
    let raw = std::fs::read(path).map_err(|e| format!("Cover image: {e}"))?;
    let format = image::guess_format(&raw).map_err(|_| "Cover image: unknown image format".to_string())?;
    let img = image::load_from_memory(&raw).map_err(|e| format!("Cover image: {e}"))?;
    let (w, h) = img.dimensions();
    let fits = max == 0 || (w <= max && h <= max);
    match format {
        ImageFormat::Jpeg if fits => return Ok((raw, "image/jpeg")),
        ImageFormat::Png if fits => return Ok((raw, "image/png")),
        _ => {}
    }
    let img = if fits { img } else { img.resize(max, max, FilterType::Lanczos3) };
    let mut buf = Vec::new();
    DynamicImage::ImageRgb8(flatten(&img, [255, 255, 255]))
        .write_with_encoder(JpegEncoder::new_with_quality(&mut buf, 90))
        .map_err(|e| e.to_string())?;
    Ok((buf, "image/jpeg"))
}
