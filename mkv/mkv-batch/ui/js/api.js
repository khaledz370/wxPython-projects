// Thin wrapper around the Rust commands (src-tauri/src/commands.rs).
const T = window.__TAURI__;

export const invoke = (cmd, args = {}) => T.core.invoke(cmd, args);
export const listen = (event, cb) => T.event.listen(event, cb);
export const appWindow = () => T.window.getCurrentWindow();

export const api = {
  settings: () => invoke('get_settings'),
  saveSettings: (settings) => invoke('save_settings', { settings }),
  toolStatus: () => invoke('tool_status'),
  languages: () => invoke('languages'),
  pickFiles: (title, filters = [], multiple = true) => invoke('pick_files', { title, filters, multiple }),
  pickFolder: (title) => invoke('pick_folder', { title }),
  /** Resolves with the full sorted list; `onBatch(entries)` gets files as soon as they are found. */
  scan: (paths, exts, recursive, onBatch) => {
    const onBatchCh = new T.core.Channel();
    onBatchCh.onmessage = (entries) => onBatch?.(entries);
    return invoke('scan_paths', { paths, exts, recursive, onBatch: onBatchCh });
  },
  identify: (path) => invoke('mkv_identify', { path }),
  muxPreview: (files, subtitles, audio, defaultLang) =>
    invoke('mux_preview', { files, subtitles, audio, defaultLang }),
  presetParse: (source, optionsFile, args) => invoke('preset_parse', { source, optionsFile, args }),
  startJob: (kind, files, options) => invoke('start_job', { kind, files, options }),
  cancelJob: (id) => invoke('cancel_job', { id }),
  pauseJob: (id, paused) => invoke('pause_job', { id, paused }),
  imageThumb: (path, size = 360) => invoke('image_thumb', { path, size }),
  audioCover: (path) => invoke('audio_cover', { path }),
  models: (settings) => invoke('translate_models', { settings }),
  testTranslate: (settings, target) => invoke('translate_test', { settings, target }),
  reveal: (path) => invoke('reveal_path', { path }),
  forceQuit: () => invoke('force_quit'),
};
