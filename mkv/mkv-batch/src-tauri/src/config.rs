//! Persistent settings (%APPDATA%\MKVBatch\settings.json) and external tool discovery.

use crate::process;
use serde::{Deserialize, Serialize};
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::Mutex;

/// What to do with a source file once a new file has replaced it.
#[derive(Serialize, Deserialize, Clone, Copy, PartialEq, Eq, Debug, Default)]
#[serde(rename_all = "lowercase")]
pub enum OriginalPolicy {
    #[default]
    Backup,
    Recycle,
    Keep,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(default, rename_all = "camelCase")]
pub struct TranslateSettings {
    /// "google" | "google_cloud" | "openai"
    pub provider: String,
    pub google_api_key: String,
    pub openai_base_url: String,
    pub openai_api_key: String,
    pub openai_model: String,
    /// Negative = do not send a temperature (some models reject it).
    pub temperature: f32,
    pub batch_size: usize,
    pub context_hint: String,
    pub timeout_secs: u64,
}

impl Default for TranslateSettings {
    fn default() -> Self {
        Self {
            provider: "google".into(),
            google_api_key: String::new(),
            openai_base_url: "http://localhost:11434/v1".into(),
            openai_api_key: String::new(),
            openai_model: String::new(),
            temperature: 0.2,
            batch_size: 25,
            context_hint: String::new(),
            timeout_secs: 180,
        }
    }
}

#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(default, rename_all = "camelCase")]
pub struct Settings {
    pub mkvtoolnix_dir: String,
    pub ffmpeg_path: String,
    pub original_policy: OriginalPolicy,
    /// Relative name = folder next to each source file, absolute path = one central folder.
    pub backup_dir: String,
    pub theme: String,
    pub translate: TranslateSettings,
}

impl Default for Settings {
    fn default() -> Self {
        Self {
            mkvtoolnix_dir: String::new(),
            ffmpeg_path: String::new(),
            original_policy: OriginalPolicy::Backup,
            backup_dir: "_originals".into(),
            theme: "dark".into(),
            translate: TranslateSettings::default(),
        }
    }
}

pub struct SettingsState(Mutex<Settings>);

impl SettingsState {
    pub fn load() -> Self {
        let settings = fs::read_to_string(settings_path())
            .ok()
            .and_then(|text| serde_json::from_str(&text).ok())
            .unwrap_or_else(|| {
                let mut s = Settings::default();
                if let Some(dir) = legacy_mkvtoolnix_dir() {
                    s.mkvtoolnix_dir = dir;
                }
                s
            });
        Self(Mutex::new(settings))
    }

    pub fn get(&self) -> Settings {
        self.0.lock().unwrap().clone()
    }

    pub fn set(&self, settings: Settings) -> Result<(), String> {
        save(&settings)?;
        *self.0.lock().unwrap() = settings;
        Ok(())
    }
}

pub fn settings_path() -> PathBuf {
    dirs::config_dir()
        .unwrap_or_else(env::temp_dir)
        .join("MKVBatch")
        .join("settings.json")
}

fn save(settings: &Settings) -> Result<(), String> {
    let path = settings_path();
    if let Some(dir) = path.parent() {
        fs::create_dir_all(dir).map_err(|e| format!("Can't create settings folder: {e}"))?;
    }
    let text = serde_json::to_string_pretty(settings).map_err(|e| e.to_string())?;
    // write-then-rename so a crash never leaves a half written settings file
    let tmp = path.with_extension("json.tmp");
    fs::write(&tmp, text).map_err(|e| format!("Can't save settings: {e}"))?;
    fs::rename(&tmp, &path).map_err(|e| format!("Can't save settings: {e}"))
}

/// Picks up the MKVToolNix folder from the old Python version's config.
fn legacy_mkvtoolnix_dir() -> Option<String> {
    let old = dirs::config_dir()?.join("mkvBatch").join("config.json");
    let value: serde_json::Value = serde_json::from_str(&fs::read_to_string(old).ok()?).ok()?;
    value["mkvtoolnix"].as_str().map(String::from)
}

pub fn which(exe: &str) -> Option<PathBuf> {
    let path = env::var_os("PATH")?;
    env::split_paths(&path)
        .map(|dir| dir.join(exe))
        .find(|candidate| candidate.is_file())
}

/// Locates mkvmerge / mkvpropedit / mkvextract.
pub fn mkvtoolnix_exe(s: &Settings, name: &str) -> Option<PathBuf> {
    let exe = format!("{name}.exe");
    let mut dirs = Vec::new();
    if !s.mkvtoolnix_dir.trim().is_empty() {
        dirs.push(PathBuf::from(s.mkvtoolnix_dir.trim()));
    }
    for var in ["ProgramW6432", "ProgramFiles", "ProgramFiles(x86)"] {
        if let Some(pf) = env::var_os(var) {
            dirs.push(PathBuf::from(pf).join("MKVToolNix"));
        }
    }
    dirs.iter()
        .map(|d| d.join(&exe))
        .find(|p| p.is_file())
        .or_else(|| which(&exe))
}

pub fn ffmpeg_exe(s: &Settings) -> Option<PathBuf> {
    let configured = s.ffmpeg_path.trim();
    if !configured.is_empty() {
        let p = PathBuf::from(configured);
        if p.is_file() {
            return Some(p);
        }
        for candidate in [p.join("ffmpeg.exe"), p.join("bin").join("ffmpeg.exe")] {
            if candidate.is_file() {
                return Some(candidate);
            }
        }
    }
    which("ffmpeg.exe").or_else(|| {
        [r"C:\ffmpeg\ffmpeg.exe", r"C:\ffmpeg\bin\ffmpeg.exe"]
            .iter()
            .map(PathBuf::from)
            .find(|p| p.is_file())
    })
}

/// First line of `<exe> <flag>`, e.g. "mkvmerge v101.0 ('Time To Turn') 64-bit".
pub fn version_line(exe: &Path, flag: &str) -> Option<String> {
    let out = process::command(exe).arg(flag).output().ok()?;
    String::from_utf8_lossy(&out.stdout)
        .lines()
        .next()
        .map(|l| l.trim().to_string())
}
