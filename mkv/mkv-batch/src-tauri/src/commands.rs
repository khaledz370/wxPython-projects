//! Everything the UI can call (`window.__TAURI__.core.invoke(name, args)`).

use crate::config::{self, Settings, SettingsState, TranslateSettings};
use crate::jobs::{JobCtx, JobRegistry, Summary};
use crate::{audio, files, images, langs, mkv, translate};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::path::{Path, PathBuf};
use tauri::ipc::Channel;
use tauri::{AppHandle, Manager, State, WebviewWindow};

/// Runs blocking work (disk, processes, HTTP) off the async runtime.
async fn blocking<T, F>(f: F) -> Result<T, String>
where
    T: Send + 'static,
    F: FnOnce() -> Result<T, String> + Send + 'static,
{
    tauri::async_runtime::spawn_blocking(f)
        .await
        .map_err(|e| e.to_string())?
}

#[tauri::command]
pub fn get_settings(state: State<'_, SettingsState>) -> Settings {
    state.get()
}

#[tauri::command]
pub fn save_settings(state: State<'_, SettingsState>, settings: Settings) -> Result<(), String> {
    state.set(settings)
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ToolInfo {
    pub id: &'static str,
    pub path: Option<String>,
    pub version: Option<String>,
}

#[tauri::command]
pub async fn tool_status(state: State<'_, SettingsState>) -> Result<Vec<ToolInfo>, String> {
    let s = state.get();
    blocking(move || {
        let info = |id: &'static str, path: Option<PathBuf>, flag: &str| ToolInfo {
            id,
            version: path.as_deref().and_then(|p| config::version_line(p, flag)),
            path: path.map(|p| p.to_string_lossy().into_owned()),
        };
        Ok(vec![
            info("mkvtoolnix", config::mkvtoolnix_exe(&s, "mkvmerge"), "--version"),
            info("ffmpeg", config::ffmpeg_exe(&s), "-version"),
        ])
    })
    .await
}

#[derive(Serialize)]
pub struct LangItem {
    code: &'static str,
    /// ISO 639-2 codes (bibliographic, terminology), used to match tracks tagged "eng", "ger"...
    alt: [&'static str; 2],
    name: &'static str,
}

#[tauri::command]
pub fn languages() -> Vec<LangItem> {
    langs::LANGS.iter().map(|l| LangItem { code: l.0, alt: [l.1, l.2], name: l.3 }).collect()
}

#[derive(Deserialize)]
pub struct Filter {
    name: String,
    extensions: Vec<String>,
}

#[tauri::command]
pub async fn pick_files(
    window: WebviewWindow,
    title: String,
    filters: Vec<Filter>,
    multiple: bool,
) -> Result<Vec<String>, String> {
    let mut dialog = rfd::FileDialog::new().set_title(&title).set_parent(&window);
    for f in &filters {
        dialog = dialog.add_filter(&f.name, &f.extensions);
    }
    let picked = if multiple {
        dialog.pick_files().unwrap_or_default()
    } else {
        dialog.pick_file().into_iter().collect()
    };
    Ok(picked.into_iter().map(|p| p.to_string_lossy().into_owned()).collect())
}

#[tauri::command]
pub async fn pick_folder(window: WebviewWindow, title: String) -> Result<Option<String>, String> {
    Ok(rfd::FileDialog::new()
        .set_title(&title)
        .set_parent(&window)
        .pick_folder()
        .map(|p| p.to_string_lossy().into_owned()))
}

#[tauri::command]
pub async fn scan_paths(
    paths: Vec<String>,
    exts: Vec<String>,
    recursive: bool,
    on_batch: Channel<Vec<files::FileEntry>>,
) -> Result<Vec<files::FileEntry>, String> {
    blocking(move || {
        Ok(files::scan(&paths, &exts, recursive, &mut |batch| {
            let _ = on_batch.send(batch);
        }))
    })
    .await
}

#[tauri::command]
pub async fn mkv_identify(state: State<'_, SettingsState>, path: String) -> Result<mkv::MkvInfo, String> {
    let s = state.get();
    blocking(move || {
        let tools = mkv::tools(&s)?;
        mkv::identify(&tools.mkvmerge, Path::new(&path))
    })
    .await
}

#[tauri::command]
pub async fn mux_preview(
    files: Vec<String>,
    subtitles: bool,
    audio: bool,
    default_lang: String,
) -> Result<Vec<mkv::MuxPreview>, String> {
    blocking(move || {
        Ok(files
            .into_iter()
            .map(|video| mkv::MuxPreview {
                sidecars: mkv::find_sidecars(Path::new(&video), subtitles, audio, &default_lang),
                video,
            })
            .collect())
    })
    .await
}

#[tauri::command]
pub async fn preset_parse(source: String, options_file: String, args: String) -> Result<Vec<String>, String> {
    blocking(move || mkv::preset_args(&source, &options_file, &args)).await
}

type JobFn = fn(&JobCtx, &Settings, &[PathBuf], Value) -> Result<Summary, String>;

fn unknown_job(_: &JobCtx, _: &Settings, _: &[PathBuf], _: Value) -> Result<Summary, String> {
    Err("Unknown job type".into())
}

#[tauri::command]
pub fn start_job(
    app: AppHandle,
    registry: State<'_, JobRegistry>,
    state: State<'_, SettingsState>,
    kind: String,
    files: Vec<String>,
    options: Value,
) -> Result<String, String> {
    if files.is_empty() {
        return Err("No files to process".into());
    }
    let settings = state.get();
    let list: Vec<PathBuf> = files.into_iter().map(PathBuf::from).collect();
    let ctx = registry.create(&app, &kind);
    let id = ctx.id.clone();

    std::thread::spawn(move || {
        let run: JobFn = match kind.as_str() {
            "remux" => mkv::remux,
            "props" => mkv::props,
            "extract" => mkv::extract,
            "mux" => mkv::mux,
            "crop" => mkv::crop,
            "preset" => mkv::preset,
            "translate" => translate::job,
            "images" => images::convert,
            "audio" => audio::job,
            _ => unknown_job,
        };
        let summary = run(&ctx, &settings, &list, options).unwrap_or_else(|e| {
            // a job-level problem (missing tool, bad options): nothing was touched
            ctx.log("error", &e);
            for i in 0..list.len() {
                ctx.status(i, "error", 0.0, &e);
            }
            Summary { failed: list.len(), ..Summary::default() }
        });
        ctx.finish(summary);
        app.state::<JobRegistry>().remove(&ctx.id);
    });
    Ok(id)
}

#[tauri::command]
pub fn cancel_job(registry: State<'_, JobRegistry>, id: String) {
    if let Some(job) = registry.get(&id) {
        job.cancel();
    }
}

#[tauri::command]
pub fn pause_job(registry: State<'_, JobRegistry>, id: String, paused: bool) {
    if let Some(job) = registry.get(&id) {
        job.set_paused(paused);
    }
}

#[tauri::command]
pub async fn image_thumb(path: String, size: u32) -> Result<images::Thumb, String> {
    blocking(move || images::thumbnail(Path::new(&path), size.clamp(64, 1024))).await
}

#[tauri::command]
pub async fn audio_cover(path: String) -> Result<Option<String>, String> {
    blocking(move || Ok(audio::cover_preview(Path::new(&path)))).await
}

#[tauri::command]
pub async fn translate_models(settings: TranslateSettings) -> Result<Vec<String>, String> {
    blocking(move || translate::list_models(&settings)).await
}

#[tauri::command]
pub async fn translate_test(settings: TranslateSettings, target: String) -> Result<String, String> {
    blocking(move || translate::test(&settings, &target)).await
}

#[tauri::command]
pub fn reveal_path(path: String) {
    files::reveal(Path::new(&path));
}

/// Called after the user confirmed closing while jobs run.
#[tauri::command]
pub fn force_quit(app: AppHandle, registry: State<'_, JobRegistry>) {
    registry.cancel_all();
    app.exit(0);
}
