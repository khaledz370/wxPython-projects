#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod audio;
mod commands;
mod config;
mod files;
mod images;
mod jobs;
mod langs;
mod mkv;
mod process;
mod subtitles;
mod translate;

use tauri::{Emitter, Manager, RunEvent, WindowEvent};

fn main() {
    let app = tauri::Builder::default()
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
            if let Some(w) = app.get_webview_window("main") {
                let _ = w.unminimize();
                let _ = w.set_focus();
            }
        }))
        .manage(config::SettingsState::load())
        .manage(jobs::JobRegistry::default())
        .invoke_handler(tauri::generate_handler![
            commands::get_settings,
            commands::save_settings,
            commands::tool_status,
            commands::languages,
            commands::pick_files,
            commands::pick_folder,
            commands::scan_paths,
            commands::mkv_identify,
            commands::mux_preview,
            commands::preset_parse,
            commands::start_job,
            commands::cancel_job,
            commands::image_thumb,
            commands::audio_cover,
            commands::translate_models,
            commands::translate_test,
            commands::reveal_path,
            commands::force_quit,
        ])
        .on_window_event(|window, event| {
            // Never close silently while mkvmerge/ffmpeg are writing files: ask the UI first.
            if let WindowEvent::CloseRequested { api, .. } = event {
                if window.app_handle().state::<jobs::JobRegistry>().any_running() {
                    api.prevent_close();
                    let _ = window.emit("confirm-close", ());
                }
            }
        })
        .build(tauri::generate_context!())
        .expect("failed to start MKV Batch");

    app.run(|handle, event| {
        if let RunEvent::Exit = event {
            handle.state::<jobs::JobRegistry>().cancel_all();
        }
    });
}
