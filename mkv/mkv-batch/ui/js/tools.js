// Tool definitions. Each tool = a page. To add an option: add a field here and the
// matching field in the Rust options struct (same name, camelCase ↔ snake_case).
import { api } from './api.js';
import { h, icon, toast, debounce, fmtSize, renderFields } from './ui.js';

export const EXT = {
  video: ['mkv', 'mp4', 'm4v', 'mov', 'avi', 'ts', 'm2ts', 'mts', 'webm', 'flv', 'ogm', 'ogv', 'mpg', 'mpeg', 'vob', '3gp', 'divx', 'mk3d'],
  matroska: ['mkv', 'mka', 'mks', 'mk3d', 'webm'],
  subs: ['srt', 'vtt', 'ass', 'ssa'],
  images: ['png', 'jpg', 'jpeg', 'jfif', 'webp', 'bmp', 'gif', 'tif', 'tiff', 'ico', 'tga', 'qoi', 'pnm', 'pbm', 'pgm', 'ppm', 'hdr'],
  audio: ['mp3', 'm4a', 'm4b', 'aac', 'flac', 'wav', 'ogg', 'oga', 'opus', 'wma', 'aiff', 'aif', 'ape', 'wv', 'mka', 'ac3', 'eac3', 'dts', 'mp2', 'caf'],
};

const isExt = (path, list) => list.includes(path.split('.').pop().toLowerCase());
const langOptions = (extra = []) => (ctx) => [...extra, ...ctx.langs.map((l) => [l.code, `${l.name} · ${l.code}`])];
const TITLE_MODES = [['keep', 'Keep as is'], ['filename', 'Use the file name'], ['clear', 'Remove the title'], ['custom', 'Custom text']];

const outputFields = (show = () => true) => [
  { type: 'select', key: 'output', label: 'Save to', default: 'subfolder', show,
    options: [['subfolder', 'Subfolder next to each file'], ['same', 'Same folder as each file'], ['folder', 'One folder…']] },
  { type: 'text', key: 'subfolder', label: 'Subfolder name', default: 'converted', show: (v) => show(v) && v.output === 'subfolder' },
  { type: 'path', key: 'folder', label: 'Output folder', mode: 'folder', show: (v) => show(v) && v.output === 'folder' },
];

function sideCard(title, ...children) {
  return h('div', { class: 'side-card' }, h('div', { class: 'side-title' }, title), ...children);
}

// ---------------------------------------------------------------------------
// Track editor (Tracks & Properties page)
// ---------------------------------------------------------------------------
function trackEditor(page) {
  const state = { tracks: [], edits: {}, file: null };
  let token = 0;
  const fileLabel = h('div', { class: 'te-file' });
  const count = h('span', { class: 'te-count' });
  const reset = h('button', { class: 'btn ghost small', type: 'button', onclick: () => { state.edits = {}; draw(); } }, icon('reset'), 'Discard edits');
  const body = h('div', { class: 'te-body' });
  const langOpts = [['und', 'Undetermined · und'], ...page.ctx.langs.map((l) => [l.code, `${l.name} · ${l.code}`])];
  // tracks tagged "eng" / "ger" show up as English / German in the list
  const norm = (code) => {
    const c = (code || 'und').toLowerCase();
    return page.ctx.langs.find((l) => l.code.toLowerCase() === c || l.alt.includes(c))?.code || code || 'und';
  };

  const edit = (sel, key, value, original) => {
    const e = state.edits[sel] || (state.edits[sel] = {});
    if (value === original) delete e[key]; else e[key] = value;
    if (!Object.keys(e).length) delete state.edits[sel];
    draw();
  };

  function draw() {
    const n = Object.keys(state.edits).length;
    count.textContent = n ? `${n} track${n === 1 ? '' : 's'} edited` : '';
    reset.disabled = !n;
    if (!state.tracks.length) {
      body.replaceChildren(h('div', { class: 'te-empty' }, state.file ? 'This file has no tracks.' : 'Click an MKV in the list to load its tracks.'));
      return;
    }
    const rows = state.tracks.map((t) => {
      const e = state.edits[t.selector] || {};
      const val = (k) => (k in e ? e[k] : k === 'language' ? norm(t.language) : t[k]);
      const cls = (k) => (k in e ? 'changed' : '');
      const options = langOpts.some(([c]) => c === val('language')) ? langOpts : [[val('language'), val('language')], ...langOpts];
      const lang = h('select', { class: cls('language'), onchange: () => edit(t.selector, 'language', lang.value, norm(t.language)) },
        options.map(([c, l]) => h('option', { value: c, selected: c === val('language') }, l)));
      const name = h('input', { type: 'text', class: cls('name'), value: val('name'), placeholder: '(no name)', spellcheck: false,
        onchange: () => edit(t.selector, 'name', name.value, t.name) });
      const flag = (k) => {
        const c = h('input', { type: 'checkbox', checked: !!val(k), onchange: () => edit(t.selector, k, c.checked, t[k]) });
        return h('label', { class: `te-flag ${cls(k)}` }, c);
      };
      const detail = t.dims || (t.channels ? `${t.channels} ch` : '');
      return h('tr', {},
        h('td', {}, h('span', { class: `sel sel-${t.kind}` }, t.selector)),
        h('td', { class: 'te-codec', title: t.codecId }, t.codec, detail ? h('span', { class: 'muted' }, ` · ${detail}`) : null),
        h('td', {}, lang), h('td', {}, name), h('td', {}, flag('default')), h('td', {}, flag('forced')), h('td', {}, flag('enabled')));
    });
    body.replaceChildren(h('div', { class: 'table-wrap' }, h('table', { class: 'te-table' },
      h('thead', {}, h('tr', {}, ...['Track', 'Codec', 'Language', 'Name', 'Default', 'Forced', 'Enabled'].map((x) => h('th', {}, x)))),
      h('tbody', {}, rows))));
  }

  page.trackEditor = {
    async load(item) {
      const my = ++token;
      if (!item) { state.tracks = []; state.file = null; fileLabel.textContent = ''; draw(); return; }
      fileLabel.textContent = `Loading ${item.name}…`;
      try {
        const info = await api.identify(item.path);
        if (my !== token) return;
        state.tracks = info.tracks;
        state.file = item;
        fileLabel.textContent = info.title ? `${item.name} · “${info.title}”` : item.name;
      } catch (e) {
        if (my !== token) return;
        state.tracks = [];
        fileLabel.textContent = `${item.name}: ${e}`;
      }
      draw();
    },
    edits: () => Object.entries(state.edits).map(([selector, e]) => ({ selector, ...e })),
  };
  draw();
  return h('div', { class: 'card track-editor' },
    h('div', { class: 'card-head' }, h('div', { class: 'card-head-text' }, h('strong', {}, 'Track editor'), fileLabel), h('span', { class: 'grow' }), count, reset),
    body);
}

// ---------------------------------------------------------------------------
// Side panels
// ---------------------------------------------------------------------------
function sidecarPanel(page) {
  const list = h('div', { class: 'sidecars' });
  const cache = new Map();
  let focused = null;
  const show = (item) => {
    focused = item;
    const cars = item ? cache.get(item.path) : null;
    if (!item) { list.replaceChildren(h('div', { class: 'muted' }, 'Select a video to see what will be merged.')); return; }
    if (!cars) { list.replaceChildren(h('div', { class: 'muted' }, 'Scanning…')); return; }
    if (!cars.length) { list.replaceChildren(h('div', { class: 'muted' }, `Nothing found next to ${item.name}.`)); return; }
    list.replaceChildren(...cars.map((c) => h('div', { class: 'sidecar' },
      h('span', { class: `sel sel-${c.kind === 'audio' ? 'audio' : 'subtitles'}` }, c.lang),
      h('div', { class: 'sidecar-main' }, h('div', { class: 'sidecar-file', title: c.path }, c.file),
        h('div', { class: 'muted small' }, [c.kind, c.forced && 'forced', c.sdh && 'SDH', c.name && `“${c.name}”`].filter(Boolean).join(' · '))))));
  };
  const refreshAll = debounce(async () => {
    const q = page.queue;
    if (!q.items.length) { show(null); return; }
    const v = page.values;
    try {
      const res = await api.muxPreview(q.items.map((i) => i.path), v.subtitles, v.audio, v.defaultLang);
      cache.clear();
      res.forEach((r, i) => {
        cache.set(r.video, r.sidecars);
        const item = q.items[i];
        if (!item) return;
        const subs = r.sidecars.filter((c) => c.kind === 'subtitles').length;
        const auds = r.sidecars.length - subs;
        item.note = r.sidecars.length ? [subs && `${subs} subtitle${subs > 1 ? 's' : ''}`, auds && `${auds} audio`].filter(Boolean).join(' + ') + ' found' : 'nothing to merge';
        q.update(i);
      });
      show(focused);
    } catch (e) { list.replaceChildren(h('div', { class: 'err-text' }, String(e))); }
  }, 250);
  page.sidecars = { show: (item) => { show(item); if (item && !cache.has(item.path)) refreshAll(); }, refreshAll };
  show(null);
  return sideCard('Files that will be merged', list,
    h('p', { class: 'field-note' }, 'Name them like the video plus a language: Movie.ar.srt, Movie.eng.ass, Movie.en.forced.srt, Movie.en.sdh.srt, Movie.jpn.mka.'));
}

function cropPanel(page) {
  const box = h('div', { class: 'crop-info muted' }, 'Select a file to see its resolution.');
  let dims = null;
  const paint = () => {
    if (!dims) return;
    const v = page.values;
    const [w, hgt] = dims;
    if (v.mode === 'clear') { box.replaceChildren(h('div', {}, `Source ${w}×${hgt}`), h('div', { class: 'muted' }, 'Crop values will be removed.')); return; }
    const nw = w - v.left - v.right;
    const nh = hgt - v.top - v.bottom;
    const bad = nw <= 0 || nh <= 0;
    box.replaceChildren(
      h('div', { class: 'crop-frame' }, h('div', { class: 'crop-inner', style: {
        top: `${(v.top / hgt) * 100}%`, bottom: `${(v.bottom / hgt) * 100}%`, left: `${(v.left / w) * 100}%`, right: `${(v.right / w) * 100}%` } })),
      h('div', {}, `Source ${w}×${hgt}  →  `, h('strong', { class: bad ? 'err-text' : '' }, bad ? 'invalid' : `${nw}×${nh}`)));
  };
  page.crop = {
    async load(item) {
      dims = null;
      if (!item) { box.textContent = 'Select a file to see its resolution.'; return; }
      box.textContent = 'Reading…';
      try {
        const info = await api.identify(item.path);
        const v = info.tracks.find((t) => t.kind === 'video');
        const m = v?.dims?.match(/(\d+)x(\d+)/);
        if (m) { dims = [Number(m[1]), Number(m[2])]; paint(); } else box.textContent = 'No video track found.';
      } catch (e) { box.textContent = String(e); }
    },
    paint,
  };
  return sideCard('Preview', box);
}

function presetPanel(page) {
  const out = h('div', { class: 'args' });
  const refresh = debounce(async () => {
    const v = page.values;
    if (v.source === 'file' && !v.optionsFile) { out.replaceChildren(h('div', { class: 'muted' }, 'Load an option file to see its settings.')); return; }
    if (v.source === 'args' && !v.args.trim()) { out.replaceChildren(h('div', { class: 'muted' }, 'Type the arguments to apply.')); return; }
    try {
      const args = await api.presetParse(v.source, v.optionsFile || '', v.args || '');
      out.replaceChildren(h('pre', { class: 'code' }, `mkvmerge -o <output> ${args.map((a) => (/\s/.test(a) || !a ? `"${a}"` : a)).join(' ')} <file>`));
    } catch (e) { out.replaceChildren(h('div', { class: 'err-text' }, String(e))); }
  }, 300);
  page.preset = { refresh };
  return sideCard('Command applied to each file', out);
}

function imagePreview(page) {
  const box = h('div', { class: 'preview muted' }, 'Select an image to preview it.');
  let token = 0;
  page.preview = async (item) => {
    const my = ++token;
    if (!item) { box.textContent = 'Select an image to preview it.'; return; }
    box.textContent = 'Loading…';
    try {
      const t = await api.imageThumb(item.path, 480);
      if (my !== token) return;
      box.replaceChildren(h('img', { src: t.dataUrl, alt: '' }), h('div', { class: 'preview-meta' }, `${t.width}×${t.height} · ${t.format} · ${fmtSize(t.size)}`));
    } catch (e) { if (my === token) box.textContent = String(e); }
  };
  return sideCard('Preview', box);
}

function audioPreview(page) {
  const current = h('div', { class: 'cover-box' });
  const chosen = h('div', { class: 'cover-box' });
  const empty = (text) => h('div', { class: 'cover-empty' }, icon('audio', 'ico big'), h('span', {}, text));
  let token = 0;
  page.coverPreview = {
    async file(item) {
      const my = ++token;
      if (!item) { current.replaceChildren(empty('No file selected')); return; }
      try {
        const url = await api.audioCover(item.path);
        if (my !== token) return;
        current.replaceChildren(url ? h('img', { src: url, alt: '' }) : empty('No embedded cover'));
      } catch { current.replaceChildren(empty('Tags not readable')); }
    },
    async chosen() {
      const v = page.values;
      if (v.cover !== 'set' || !v.coverPath) { chosen.parentElement.hidden = true; return; }
      chosen.parentElement.hidden = false;
      try {
        const t = await api.imageThumb(v.coverPath, 320);
        chosen.replaceChildren(h('img', { src: t.dataUrl, alt: '' }), h('div', { class: 'preview-meta' }, `${t.width}×${t.height} · ${t.format}`));
      } catch (e) { chosen.replaceChildren(h('div', { class: 'err-text' }, String(e))); }
    },
  };
  current.replaceChildren(empty('No file selected'));
  const chosenCard = sideCard('New cover', chosen);
  const wrap = h('div', { class: 'side-stack' }, sideCard('Current cover', current), chosenCard);
  setTimeout(() => page.coverPreview.chosen(), 0);
  return wrap;
}

// ---------------------------------------------------------------------------
// Translation engine panel (bound to settings.translate)
// ---------------------------------------------------------------------------
const AI_PRESETS = [
  ['Ollama', 'http://localhost:11434/v1'],
  ['LM Studio', 'http://localhost:1234/v1'],
  ['llama.cpp', 'http://localhost:8080/v1'],
  ['OpenAI', 'https://api.openai.com/v1'],
  ['OpenRouter', 'https://openrouter.ai/api/v1'],
  ['Gemini', 'https://generativelanguage.googleapis.com/v1beta/openai'],
  ['Groq', 'https://api.groq.com/openai/v1'],
];

function enginePanel(page) {
  const ctx = page.ctx;
  const t = ctx.settings.translate;
  const save = debounce(() => ctx.saveSettings(), 400);
  const root = h('div', { class: 'fields' });
  const result = h('div', { class: 'test-result muted' });
  const isAi = (v) => v.provider === 'openai';

  const fields = [
    { type: 'segmented', key: 'provider', label: 'Engine', options: [['google', 'Google'], ['google_cloud', 'Google Cloud'], ['openai', 'AI model']] },
    { type: 'note', text: 'Free Google Translate, no key needed. Fine for normal use; very large batches can get rate-limited.', show: (v) => v.provider === 'google' },
    { type: 'password', key: 'googleApiKey', label: 'Google Cloud API key', show: (v) => v.provider === 'google_cloud' },
    { type: 'custom', label: 'Server', show: isAi, render: (v, set) => h('div', { class: 'preset-chips' },
      AI_PRESETS.map(([name, url]) => h('button', { type: 'button', class: `chip-btn${v.openaiBaseUrl === url ? ' on' : ''}`, onclick: () => { set('openaiBaseUrl', url); draw(); } }, name))) },
    { type: 'text', key: 'openaiBaseUrl', label: 'Base URL (OpenAI-compatible)', placeholder: 'http://localhost:11434/v1', show: isAi },
    { type: 'password', key: 'openaiApiKey', label: 'API key', placeholder: 'not needed for local servers', show: isAi },
    { type: 'custom', label: 'Model', show: isAi, render: (v, set) => {
      const listId = 'models-list';
      const input = h('input', { type: 'text', value: v.openaiModel, list: listId, placeholder: 'e.g. qwen2.5:14b, gpt-4o-mini', spellcheck: false, oninput: () => set('openaiModel', input.value) });
      const dl = h('datalist', { id: listId });
      const load = h('button', { class: 'btn small', type: 'button', onclick: async () => {
        load.disabled = true;
        try {
          const models = await api.models(t);
          dl.replaceChildren(...models.map((m) => h('option', { value: m })));
          toast(models.length ? `${models.length} models available, pick one from the list` : 'The server returned no models', 'info');
          input.focus();
        } catch (e) { toast(String(e), 'error'); }
        load.disabled = false;
      } }, icon('refresh'), 'List');
      return h('div', { class: 'path-input' }, input, dl, load);
    } },
    { type: 'row', show: isAi, children: [
      { type: 'number', key: 'batchSize', label: 'Lines / request', min: 1, max: 200 },
      { type: 'number', key: 'timeoutSecs', label: 'Timeout (s)', min: 10, max: 1800 },
    ] },
    { type: 'range', key: 'temperature', label: 'Temperature', min: 0, max: 1, step: 0.05, show: isAi },
    { type: 'textarea', key: 'contextHint', label: 'Extra instructions', rows: 3, show: isAi,
      placeholder: 'e.g. Anime series, keep Japanese honorifics. Use Modern Standard Arabic.' },
  ];

  function draw() {
    root.replaceChildren();
    renderFields(root, fields, t, () => save(), { api, langs: ctx.langs });
  }
  draw();
  const test = h('button', { class: 'btn small', type: 'button', onclick: async () => {
    test.disabled = true;
    result.className = 'test-result muted';
    result.textContent = 'Testing…';
    try {
      await ctx.saveSettings();
      const out = await api.testTranslate(t, page.values.target || 'ar');
      result.className = 'test-result ok-text';
      result.textContent = `✓ ${out}`;
    } catch (e) {
      result.className = 'test-result err-text';
      result.textContent = String(e);
    }
    test.disabled = false;
  } }, icon('check'), 'Test engine');
  return sideCard('Engine', root, h('div', { class: 'test-row' }, test), result);
}

// ---------------------------------------------------------------------------
// The tools
// ---------------------------------------------------------------------------
export const TOOLS = [
  {
    id: 'remux', job: 'remux', group: 'Matroska', label: 'Remux', icon: 'remux', requires: 'mkvtoolnix',
    title: 'Remux to MKV', startLabel: 'Remux',
    blurb: 'Rewrap MP4, AVI, TS, MOV or MKV into Matroska without re-encoding. Drop unwanted languages, fix default tracks and strip extras in the same pass.',
    accept: EXT.video, acceptLabel: 'MKV · MP4 · AVI · TS · M2TS · MOV · WebM · FLV · MPG · VOB',
    fields: [
      { type: 'heading', label: 'Keep tracks' },
      { type: 'text', key: 'audioLangs', label: 'Audio languages', placeholder: 'all, or e.g. jpn, eng', hint: 'Files with no matching audio are skipped, never made silent.' },
      { type: 'text', key: 'subtitleLangs', label: 'Subtitle languages', placeholder: 'all, or e.g. ara, eng' },
      { type: 'heading', label: 'Default tracks' },
      { type: 'select', key: 'defaultAudio', label: 'Default audio', options: langOptions([['', 'Leave as is']]), default: '' },
      { type: 'select', key: 'defaultSubtitle', label: 'Default subtitles', options: langOptions([['', 'Leave as is'], ['none', 'No default subtitle']]), default: '' },
      { type: 'heading', label: 'Clean up' },
      { type: 'check', key: 'noAttachments', label: 'Remove attachments', hint: 'fonts, cover images' },
      { type: 'check', key: 'noChapters', label: 'Remove chapters' },
      { type: 'check', key: 'noGlobalTags', label: 'Remove global tags' },
      { type: 'heading', label: 'Title & chapters' },
      { type: 'select', key: 'titleMode', label: 'Title', options: TITLE_MODES },
      { type: 'text', key: 'title', label: 'Custom title', show: (v) => v.titleMode === 'custom' },
      { type: 'number', key: 'chapterMinutes', label: 'Chapter every … minutes', min: 0, max: 600, hint: '0 = off. Replaces existing chapters.' },
    ],
  },
  {
    id: 'props', job: 'props', group: 'Matroska', label: 'Tracks & Tags', icon: 'props', requires: 'mkvtoolnix',
    title: 'Tracks & Properties', startLabel: 'Apply changes',
    blurb: 'Edit track languages, names and default / forced flags, set the title, add a cover, strip chapters, tags or attachments. Written straight into the MKV header in a second, with no remux.',
    accept: EXT.matroska, acceptLabel: 'MKV · MKA · MKS · WebM',
    fields: [
      { type: 'heading', label: 'File' },
      { type: 'select', key: 'titleMode', label: 'Title', options: TITLE_MODES },
      { type: 'text', key: 'title', label: 'Custom title', show: (v) => v.titleMode === 'custom' },
      { type: 'path', key: 'cover', label: 'Cover image', mode: 'file', filters: [{ name: 'Images', extensions: EXT.images }], placeholder: 'none', hint: 'Stored as the cover.jpg attachment. Replaces an existing cover.' },
      { type: 'heading', label: 'Remove' },
      { type: 'check', key: 'deleteChapters', label: 'Chapters' },
      { type: 'check', key: 'deleteTags', label: 'All tags' },
      { type: 'check', key: 'deleteAttachments', label: 'All attachments', hint: 'includes fonts used by ASS subtitles' },
      { type: 'note', text: 'Track edits from the editor are applied to every file by position (a1 = first audio track), which suits episodes of one release.' },
    ],
    main: (page) => trackEditor(page),
    onFocus: (item, page) => page.trackEditor.load(item),
    collect: (v, page) => ({ ...v, edits: page.trackEditor.edits() }),
    onDrop: (paths, page) => {
      const img = paths.find((p) => isExt(p, EXT.images));
      if (img) { page.setValues({ cover: img }); toast('Cover image set', 'ok', 1800); }
      return paths.filter((p) => !isExt(p, EXT.images));
    },
  },
  {
    id: 'extract', job: 'extract', group: 'Matroska', label: 'Extract', icon: 'extract', requires: 'mkvtoolnix',
    title: 'Extract Tracks', startLabel: 'Extract',
    blurb: 'Pull audio, subtitles, video, attachments (fonts) and chapters out of MKV files into separate files, named by track and language.',
    accept: EXT.matroska, acceptLabel: 'MKV · MKA · MKS · WebM',
    fields: [
      { type: 'heading', label: 'What to extract' },
      { type: 'check', key: 'audio', label: 'Audio tracks', default: true },
      { type: 'check', key: 'audioAsMka', label: 'All audio into one .mka file', hint: 'instead of raw streams (.aac, .ac3, .flac…)', show: (v) => v.audio },
      { type: 'check', key: 'subtitles', label: 'Subtitle tracks', default: true },
      { type: 'check', key: 'video', label: 'Video track' },
      { type: 'check', key: 'attachments', label: 'Attachments', hint: 'fonts, covers' },
      { type: 'check', key: 'chapters', label: 'Chapters (XML)' },
      { type: 'text', key: 'langs', label: 'Only these languages', placeholder: 'all, or e.g. ara, eng', hint: 'Applies to audio and subtitle tracks.' },
      { type: 'heading', label: 'Output' },
      { type: 'path', key: 'outDir', mode: 'folder', label: 'Output folder', placeholder: 'next to each file, in <name>_extracted' },
    ],
    validate: (v) => (v.audio || v.subtitles || v.video || v.attachments || v.chapters ? null : 'Pick at least one thing to extract.'),
  },
  {
    id: 'mux', job: 'mux', group: 'Matroska', label: 'Add Subtitles', icon: 'mux', requires: 'mkvtoolnix',
    title: 'Add Subtitles & Audio', startLabel: 'Merge',
    blurb: 'Merge the subtitle and audio files that sit next to each video into it. Languages and forced / SDH flags come from the file names, text encodings are detected automatically.',
    accept: EXT.video, acceptLabel: 'Videos: MKV · MP4 · AVI · TS · MOV…',
    fields: [
      { type: 'heading', label: 'Look for' },
      { type: 'check', key: 'subtitles', label: 'Subtitles', hint: 'srt, ass, ssa, vtt, sup, idx/sub', default: true },
      { type: 'check', key: 'audio', label: 'Audio', hint: 'mka, aac, ac3, eac3, dts, flac, mp3, opus…' },
      { type: 'select', key: 'defaultLang', label: 'Language when the name has none', options: langOptions([['und', 'Undetermined']]), default: 'und' },
      { type: 'heading', label: 'Tracks' },
      { type: 'check', key: 'makeDefault', label: 'Make the first added subtitle the default', default: true },
      { type: 'check', key: 'removeExistingSubs', label: 'Replace the existing subtitle tracks' },
      { type: 'check', key: 'disposeSidecars', label: 'Move merged files away afterwards', hint: 'follows the backup / Recycle Bin rule in Settings' },
    ],
    side: (page) => sidecarPanel(page),
    onFocus: (item, page) => page.sidecars.show(item),
    onQueueChange: (page) => page.sidecars.refreshAll(),
    onValues: (page) => page.sidecars.refreshAll(),
    afterJob: (page) => page.sidecars.refreshAll(),
  },
  {
    id: 'crop', job: 'crop', group: 'Matroska', label: 'Crop', icon: 'crop', requires: 'mkvtoolnix',
    title: 'Crop', startLabel: 'Apply',
    blurb: 'Set Matroska pixel-crop values so players hide black bars without re-encoding. MKV files change instantly in place; other formats are remuxed to MKV with the crop.',
    accept: EXT.video, acceptLabel: 'MKV · MP4 · AVI · TS · MOV…',
    fields: [
      { type: 'segmented', key: 'mode', label: 'Action', options: [['set', 'Set crop'], ['clear', 'Remove crop']] },
      { type: 'row', label: 'Pixels to crop', show: (v) => v.mode === 'set', children: [
        { type: 'number', key: 'top', label: 'Top', min: 0, max: 8000 },
        { type: 'number', key: 'right', label: 'Right', min: 0, max: 8000 },
        { type: 'number', key: 'bottom', label: 'Bottom', min: 0, max: 8000 },
        { type: 'number', key: 'left', label: 'Left', min: 0, max: 8000 },
      ] },
      { type: 'note', text: 'mpv, VLC and MPC-HC honour pixel crop. Some TVs and hardware players ignore it.' },
    ],
    side: (page) => cropPanel(page),
    onFocus: (item, page) => page.crop.load(item),
    onValues: (page) => page.crop.paint(),
    collect: (v) => ({ top: v.top, right: v.right, bottom: v.bottom, left: v.left, clear: v.mode === 'clear' }),
    validate: (v) => (v.mode === 'set' && !(v.top || v.right || v.bottom || v.left) ? 'Enter at least one crop value.' : null),
  },
  {
    id: 'preset', job: 'preset', group: 'Matroska', label: 'Custom mkvmerge', icon: 'preset', requires: 'mkvtoolnix',
    title: 'Custom mkvmerge Preset', startLabel: 'Run preset',
    blurb: 'Apply the same mkvmerge settings to many files: load an option file saved from MKVToolNix GUI (Multiplexer → Create option file) or type the arguments yourself.',
    accept: EXT.video, acceptLabel: 'MKV · MP4 · AVI · TS · MOV…',
    fields: [
      { type: 'segmented', key: 'source', label: 'Preset from', options: [['file', 'Option file (.json)'], ['args', 'Typed arguments']] },
      { type: 'path', key: 'optionsFile', label: 'MKVToolNix option file', mode: 'file', filters: [{ name: 'Option files', extensions: ['json'] }], show: (v) => v.source === 'file' },
      { type: 'textarea', key: 'args', label: 'mkvmerge arguments', rows: 5, show: (v) => v.source === 'args',
        placeholder: '--no-attachments --audio-tracks jpn --default-track-flag 2:yes', hint: 'Leave out -o and the input file; they are added for every file.' },
    ],
    side: (page) => presetPanel(page),
    init: (page) => page.preset.refresh(),
    onValues: (page) => page.preset.refresh(),
    onDrop: (paths, page) => {
      const json = paths.find((p) => isExt(p, ['json']));
      if (json) { page.setValues({ source: 'file', optionsFile: json }); toast('Option file loaded', 'ok', 1800); }
      return paths.filter((p) => !isExt(p, ['json']));
    },
  },
  {
    id: 'translate', job: 'translate', group: 'Subtitles', label: 'Translate', icon: 'translate', requires: null,
    title: 'Translate Subtitles', startLabel: 'Translate',
    blurb: 'Translate SRT, VTT and ASS files, or the subtitle track inside MKV files, with Google or any OpenAI-compatible AI, including local models in Ollama or LM Studio. Timing and styling stay intact.',
    accept: [...EXT.subs, ...EXT.matroska], acceptLabel: 'SRT · VTT · ASS · SSA · MKV with text subtitles',
    fields: [
      { type: 'heading', label: 'Languages' },
      { type: 'select', key: 'source', label: 'From', options: langOptions([['auto', 'Detect automatically']]), default: 'auto' },
      { type: 'select', key: 'target', label: 'To', options: langOptions(), default: 'ar' },
      { type: 'heading', label: 'MKV files' },
      { type: 'text', key: 'trackLang', label: 'Track to translate', placeholder: 'first text track, or a language e.g. eng' },
      { type: 'check', key: 'muxBack', label: 'Add the translation to the MKV as a new track', hint: 'otherwise saved as Movie.<lang>.srt next to it' },
      { type: 'check', key: 'setDefault', label: 'Make it the default subtitle', show: (v) => v.muxBack },
    ],
    side: (page) => enginePanel(page),
    validate: (v) => (!v.target ? 'Choose a target language.' : v.source === v.target ? 'Source and target language are the same.' : null),
    beforeStart: async (page) => { await page.ctx.saveSettings(); },
  },
  {
    id: 'images', job: 'images', group: 'Media', label: 'Images', icon: 'image', requires: null,
    title: 'Image Converter', startLabel: 'Convert',
    blurb: 'Convert between PNG, JPG, WebP, BMP, GIF, TIFF, ICO, TGA and QOI, resize, and fix phone photo rotation. Uses every CPU core.',
    accept: EXT.images, acceptLabel: 'PNG · JPG · WebP · BMP · GIF · TIFF · ICO · TGA · QOI · HDR · PNM',
    fields: [
      { type: 'heading', label: 'Format' },
      { type: 'select', key: 'format', label: 'Convert to', default: 'webp', options: [
        ['png', 'PNG · lossless'], ['jpg', 'JPG'], ['webp', 'WebP'], ['bmp', 'BMP'], ['gif', 'GIF · first frame'],
        ['tiff', 'TIFF'], ['ico', 'ICO · multi-size icon'], ['tga', 'TGA'], ['qoi', 'QOI']] },
      { type: 'check', key: 'webpLossless', label: 'Lossless WebP', show: (v) => v.format === 'webp' },
      { type: 'range', key: 'quality', label: 'Quality', min: 1, max: 100, default: 85, show: (v) => v.format === 'jpg' || (v.format === 'webp' && !v.webpLossless) },
      { type: 'color', key: 'background', label: 'Fill transparent areas with', default: '#ffffff', show: (v) => v.format === 'jpg' },
      { type: 'check', key: 'autoOrient', label: 'Rotate using EXIF orientation', default: true },
      { type: 'heading', label: 'Size' },
      { type: 'segmented', key: 'resize', label: 'Resize', options: [['none', 'Original'], ['fit', 'Fit inside'], ['percent', 'Scale %']] },
      { type: 'row', show: (v) => v.resize === 'fit', children: [
        { type: 'number', key: 'maxWidth', label: 'Max width', min: 1, max: 30000, default: 1920 },
        { type: 'number', key: 'maxHeight', label: 'Max height', min: 1, max: 30000, default: 1920 },
      ] },
      { type: 'range', key: 'percent', label: 'Scale (%)', min: 5, max: 400, default: 50, show: (v) => v.resize === 'percent' },
      { type: 'heading', label: 'Output' },
      ...outputFields(),
      { type: 'check', key: 'overwrite', label: 'Replace files with the same name', hint: 'the source image itself is never overwritten' },
      { type: 'number', key: 'threads', label: 'Parallel jobs', min: 0, max: 64, hint: '0 = all CPU cores' },
    ],
    side: (page) => imagePreview(page),
    onFocus: (item, page) => page.preview(item),
    validate: (v) => (v.output === 'folder' && !v.folder ? 'Choose the output folder.' : null),
  },
  {
    id: 'audio', job: 'audio', group: 'Media', label: 'Audio', icon: 'audio', requires: 'ffmpeg',
    title: 'Audio Converter & Cover Art', startLabel: 'Process',
    blurb: 'Convert audio, or the audio of videos, to MP3, AAC, Opus, Ogg, FLAC, WAV or ALAC, and embed, replace, remove or save cover art. Cover changes only touch the tags, the audio is never re-encoded for them.',
    accept: [...EXT.audio, ...EXT.video], acceptLabel: 'MP3 · M4A · FLAC · WAV · OGG · OPUS · WMA · AIFF · APE… and videos',
    fields: [
      { type: 'heading', label: 'Conversion' },
      { type: 'check', key: 'convert', label: 'Convert format', default: true, hint: 'turn off to only change covers of the files in place' },
      { type: 'select', key: 'format', label: 'Format', default: 'mp3', show: (v) => v.convert, options: [
        ['mp3', 'MP3'], ['m4a', 'AAC (.m4a)'], ['opus', 'Opus'], ['ogg', 'Ogg Vorbis'], ['flac', 'FLAC · lossless'], ['alac', 'ALAC (.m4a) · lossless'], ['wav', 'WAV · 16-bit PCM']] },
      { type: 'select', key: 'bitrate', label: 'Bitrate', numeric: true, default: 0, show: (v) => v.convert && ['mp3', 'm4a', 'opus', 'ogg'].includes(v.format), options: [
        [0, 'Auto (high quality)'], [96, '96 kbps'], [128, '128 kbps'], [160, '160 kbps'], [192, '192 kbps'], [256, '256 kbps'], [320, '320 kbps']] },
      { type: 'row', show: (v) => v.convert, children: [
        { type: 'select', key: 'sampleRate', label: 'Sample rate', numeric: true, default: 0, options: [[0, 'Keep'], [44100, '44.1 kHz'], [48000, '48 kHz'], [96000, '96 kHz']] },
        { type: 'select', key: 'channels', label: 'Channels', numeric: true, default: 0, options: [[0, 'Keep'], [1, 'Mono'], [2, 'Stereo']] },
      ] },
      ...outputFields((v) => v.convert),
      { type: 'heading', label: 'Cover art' },
      { type: 'select', key: 'cover', label: 'Cover', default: 'keep', options: [
        ['keep', 'Keep the existing cover'], ['set', 'Set one image for all files'], ['auto', 'Use the image in each folder'], ['remove', 'Remove covers'], ['extract', 'Save the embedded cover as an image']] },
      { type: 'path', key: 'coverPath', label: 'Cover image', mode: 'file', filters: [{ name: 'Images', extensions: EXT.images }], show: (v) => v.cover === 'set', hint: 'Tip: drop an image on this page.' },
      { type: 'note', text: 'Uses Song.jpg next to Song.mp3, otherwise a cover, folder, front or album image (.jpg .png .webp).', show: (v) => v.cover === 'auto' },
      { type: 'select', key: 'coverMax', label: 'Resize cover to', numeric: true, default: 1200, show: (v) => v.cover === 'set' || v.cover === 'auto', options: [
        [0, 'Original size'], [600, '600 px'], [1000, '1000 px'], [1200, '1200 px'], [1500, '1500 px']] },
      { type: 'heading', label: 'Performance' },
      { type: 'number', key: 'threads', label: 'Parallel jobs', min: 1, max: 16, default: 2 },
    ],
    side: (page) => audioPreview(page),
    onFocus: (item, page) => page.coverPreview.file(item),
    onValues: (page, key) => { if (key === 'cover' || key === 'coverPath') page.coverPreview.chosen(); },
    validate: (v) => {
      if (!v.convert && v.cover === 'keep') return 'Nothing to do: turn on conversion or choose a cover action.';
      if (v.cover === 'set' && !v.coverPath) return 'Choose the cover image.';
      if (v.convert && v.output === 'folder' && !v.folder) return 'Choose the output folder.';
      return null;
    },
    onDrop: (paths, page) => {
      const img = paths.find((p) => isExt(p, EXT.images));
      if (img) { page.setValues({ cover: 'set', coverPath: img }); toast('Cover image set', 'ok', 1800); }
      return paths.filter((p) => !isExt(p, EXT.images));
    },
  },
];
