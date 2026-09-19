// Settings page: tool locations, what happens to originals, appearance.
import { api } from './api.js';
import { h, icon, renderFields, debounce } from './ui.js';

export class SettingsPage {
  constructor(ctx) {
    this.ctx = ctx;
    this.tool = { id: 'settings', title: 'Settings' };
    this.el = this.build();
  }

  build() {
    const ctx = this.ctx;
    const s = ctx.settings;
    const saveSoon = debounce(async () => { await ctx.saveSettings(); ctx.refreshTools(); }, 500);
    this.statusBox = h('div', { class: 'tool-tiles' });

    const form = h('div', { class: 'fields' });
    renderFields(form, [
      { type: 'heading', label: 'External programs' },
      { type: 'path', key: 'mkvtoolnixDir', label: 'MKVToolNix folder', mode: 'folder', placeholder: 'auto-detect (C:\\Program Files\\MKVToolNix, PATH)' },
      { type: 'path', key: 'ffmpegPath', label: 'ffmpeg.exe', mode: 'file', filters: [{ name: 'ffmpeg', extensions: ['exe'] }], placeholder: 'auto-detect (PATH, C:\\ffmpeg)' },
      { type: 'heading', label: 'Safety' },
      { type: 'segmented', key: 'originalPolicy', label: 'When a new file replaces its source, the original goes to',
        options: [['backup', 'Backup folder'], ['recycle', 'Recycle Bin'], ['keep', 'Stays (new file renamed)'], ['folder', 'Specific folder']] },
      { type: 'path', key: 'backupFolder', label: 'Put backups in', mode: 'folder', placeholder: 'e.g. C:\\Users\\you\\Downloads', show: (v) => v.originalPolicy === 'folder',
        hint: 'A backup folder (named below) is created inside this folder and every original goes there. Moving to another drive copies the file, which takes longer.' },
      { type: 'text', key: 'backupDir', label: 'Backup folder name', placeholder: 'mkv_old', show: (v) => v.originalPolicy === 'backup' || v.originalPolicy === 'folder',
        hint: 'Backup folder: used at the source drive root, or as a central folder when you enter an absolute path. The sidebar toggle chooses same directory or root.' },
      { type: 'segmented', key: 'backupIcon', label: 'Backup folder icon', show: (v) => v.originalPolicy === 'backup' || v.originalPolicy === 'folder',
        options: [['trash', 'Red trash'], ['none', 'Default folder']],
        hint: 'Stamps the backup folder with a custom icon in Explorer.' },
      { type: 'note', text: 'Every tool writes to a temporary file first and only swaps it in after the job finished successfully. Failures and Cancel never touch your originals, and the free disk space is checked before remuxing.' },
      { type: 'heading', label: 'Speed' },
      { type: 'number', key: 'parallelFiles', label: 'Files at the same time', min: 1, max: 16,
        hint: 'Remux, tracks, extract, add subtitles, crop, properties and presets. mkvmerge uses one CPU core per file, so 2-4 is faster on big batches. Keep it low for files on a network share or a hard disk.' },
      { type: 'heading', label: 'Appearance' },
      { type: 'segmented', key: 'theme', label: 'Theme', options: [['dark', 'Dark'], ['light', 'Light']] },
    ], s, (key) => {
      if (key === 'theme') ctx.applyTheme(s.theme);
      saveSoon();
    }, { api });

    return h('section', { class: 'page settings-page', 'data-tool': 'settings', hidden: true },
      h('header', { class: 'page-head' }, h('div', {},
        h('div', { class: 'eyebrow' }, 'App'),
        h('h1', {}, 'Settings'),
        h('p', {}, 'Saved automatically to %APPDATA%\\MKVBatch\\settings.json.'))),
      h('div', { class: 'settings-body' },
        h('div', { class: 'card settings-card' },
          h('div', { class: 'card-head' }, h('strong', {}, 'Programs found'), h('span', { class: 'grow' }),
            h('button', { class: 'btn ghost small', type: 'button', onclick: () => ctx.refreshTools() }, icon('refresh'), 'Check again')),
          this.statusBox),
        h('div', { class: 'card settings-card' }, form)));
  }

  setToolStatus(status) {
    const names = { mkvtoolnix: ['MKVToolNix', 'Remux, tracks, extract, subtitles, crop, presets. Free at mkvtoolnix.download'],
      ffmpeg: ['ffmpeg', 'Audio conversion. Free at ffmpeg.org (gyan.dev builds for Windows)'] };
    this.statusBox.replaceChildren(...status.map((t) => h('div', { class: `tool-tile ${t.path ? 'ok' : 'bad'}` },
      h('div', { class: 'tile-dot' }),
      h('div', { class: 'tile-text' },
        h('strong', {}, names[t.id][0]),
        h('div', { class: 'small' }, t.version || 'Not found'),
        h('div', { class: 'muted small mono' }, t.path || names[t.id][1])))));
  }
}
