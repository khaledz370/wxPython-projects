// Small DOM toolkit: element builder, icons, toasts, dialogs and the options form renderer.

export function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === undefined || v === null || v === false) continue;
    if (k === 'class') el.className = v;
    else if (k === 'style' && typeof v === 'object') Object.assign(el.style, v);
    else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
    else if (k === 'html') el.innerHTML = v;
    else if (k in el && typeof v !== 'string') el[k] = v;
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const c of children.flat()) {
    if (c === null || c === undefined || c === false) continue;
    el.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return el;
}

const PATHS = {
  remux: '<path d="M4 8h12l-3-3"/><path d="M20 16H8l3 3"/>',
  props: '<path d="M4 6h9M17 6h3M4 12h3M11 12h9M4 18h11M19 18h1"/><circle cx="15" cy="6" r="2"/><circle cx="9" cy="12" r="2"/><circle cx="17" cy="18" r="2"/>',
  extract: '<path d="M4 14v5a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-5"/><path d="M12 15V3M7 8l5-5 5 5"/>',
  mux: '<path d="M12 3 3 8l9 5 9-5z"/><path d="M3 13l9 5 9-5"/>',
  crop: '<path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/>',
  preset: '<path d="M4 6l6 6-6 6M12 18h8"/>',
  translate: '<path d="M4 5h9M8.5 3v2M6 5c1 4 4 7 7 8M11 5c-1 4-4 7-7 8"/><path d="M13 21l4-9 4 9M14.5 18h5"/>',
  image: '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-9 9"/>',
  audio: '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
  settings: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1 7 17M17 7l2.1-2.1"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  folder: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
  trash: '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
  play: '<path d="M7 4l13 8-13 8z"/>',
  stop: '<rect x="6" y="6" width="12" height="12" rx="1.5"/>',
  log: '<path d="M5 4h14v16H5zM9 8h6M9 12h6M9 16h4"/>',
  x: '<path d="M6 6l12 12M18 6 6 18"/>',
  check: '<path d="M5 12l5 5 9-10"/>',
  reset: '<path d="M4 12a8 8 0 1 0 2.3-5.6M4 4v4h4"/>',
  open: '<path d="M14 4h6v6M20 4l-8 8M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
  sweep: '<path d="M4 20h16M7 16l3-9 7 3-3 6"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
  refresh: '<path d="M20 12a8 8 0 1 1-2.3-5.6M20 4v4h-4"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
};

export function icon(name, cls = 'ico') {
  const span = document.createElement('span');
  span.className = 'ico-wrap';
  span.innerHTML = `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true">${PATHS[name] || ''}</svg>`;
  return span;
}

/** Replaces <span data-icon="name"> placeholders in static HTML. */
export function hydrateIcons(root = document) {
  root.querySelectorAll('[data-icon]').forEach((el) => {
    el.replaceWith(icon(el.dataset.icon));
  });
}

export function fmtSize(n) {
  if (!n && n !== 0) return '';
  const u = ['B', 'KB', 'MB', 'GB', 'TB'];
  let i = 0;
  let v = n;
  while (v >= 1024 && i < u.length - 1) { v /= 1024; i++; }
  return i === 0 ? `${n} B` : `${v.toFixed(v < 10 ? 2 : 1)} ${u[i]}`;
}

export function fmtTime(ms) {
  const s = Math.floor(ms / 1000);
  const m = Math.floor(s / 60);
  return m ? `${m}m ${String(s % 60).padStart(2, '0')}s` : `${s}s`;
}

export function debounce(fn, ms = 300) {
  let t;
  return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}

export function toast(text, kind = 'info', ms = 4200) {
  const el = h('div', { class: `toast ${kind}` }, icon(kind === 'error' ? 'x' : kind === 'ok' ? 'check' : 'info'), h('div', {}, text));
  document.getElementById('toasts').append(el);
  setTimeout(() => el.classList.add('out'), ms);
  setTimeout(() => el.remove(), ms + 400);
}

export function confirmDialog({ title, text, ok = 'OK', cancel = 'Cancel', danger = false }) {
  return new Promise((resolve) => {
    const root = document.getElementById('modalRoot');
    const close = (v) => { overlay.remove(); resolve(v); };
    const overlay = h('div', { class: 'modal-overlay', onclick: (e) => { if (e.target === overlay) close(false); } },
      h('div', { class: 'modal' },
        h('h2', {}, title),
        h('p', {}, text),
        h('div', { class: 'modal-actions' },
          h('button', { class: 'btn ghost', type: 'button', onclick: () => close(false) }, cancel),
          h('button', { class: `btn ${danger ? 'danger-solid' : 'primary'}`, type: 'button', onclick: () => close(true) }, ok))));
    root.append(overlay);
    overlay.querySelector('.modal-actions .btn:last-child').focus();
  });
}

/**
 * Renders a declarative list of option fields.
 * Field types: heading, note, check, select, segmented, text, textarea, number, range, color, path, row.
 * `show(values)` hides a field when it returns false. Returns { refresh } to re-evaluate visibility.
 */
export function renderFields(root, fields, values, onChange, ctx = {}) {
  const entries = [];
  const set = (key, value) => { values[key] = value; onChange(key, value); refresh(); };
  const opts = (f) => (typeof f.options === 'function' ? f.options(ctx) : f.options);

  const build = (f) => {
    const label = f.label ? h('label', { class: 'lbl' }, f.label) : null;
    const hint = f.hint ? h('div', { class: 'hint' }, f.hint) : null;
    let control;
    switch (f.type) {
      case 'heading':
        return h('div', { class: 'field-heading' }, f.label);
      case 'note':
        return h('p', { class: 'field-note' }, f.text);
      case 'check': {
        const input = h('input', { type: 'checkbox', checked: !!values[f.key], onchange: () => set(f.key, input.checked) });
        return h('div', { class: 'field' }, h('label', { class: 'check' }, input, h('span', {}, f.label, hint)));
      }
      case 'select': {
        control = h('select', { onchange: () => set(f.key, control.value) },
          opts(f).map(([v, l]) => h('option', { value: v, selected: String(values[f.key]) === String(v) }, l)));
        if (f.numeric) control.onchange = () => set(f.key, Number(control.value));
        break;
      }
      case 'segmented': {
        control = h('div', { class: 'seg' });
        const paint = () => control.querySelectorAll('button').forEach((b) => b.classList.toggle('on', b.dataset.v === String(values[f.key])));
        opts(f).forEach(([v, l]) => control.append(h('button', { type: 'button', 'data-v': String(v), onclick: () => { set(f.key, v); paint(); } }, l)));
        paint();
        break;
      }
      case 'text':
      case 'password':
        control = h('input', { type: f.type, value: values[f.key] ?? '', placeholder: f.placeholder || '', spellcheck: false, oninput: () => set(f.key, control.value) });
        break;
      case 'textarea':
        control = h('textarea', { rows: f.rows || 4, placeholder: f.placeholder || '', spellcheck: false, oninput: () => set(f.key, control.value) });
        control.value = values[f.key] ?? '';
        break;
      case 'number':
        control = h('input', { type: 'number', value: values[f.key] ?? 0, min: f.min, max: f.max, step: f.step || 1, oninput: () => set(f.key, Number(control.value) || 0) });
        break;
      case 'range': {
        const out = h('span', { class: 'range-val' }, String(values[f.key]));
        const input = h('input', { type: 'range', min: f.min, max: f.max, step: f.step || 1, value: values[f.key], oninput: () => { out.textContent = input.value; set(f.key, Number(input.value)); } });
        control = h('div', { class: 'range' }, input, out);
        break;
      }
      case 'color':
        control = h('input', { type: 'color', value: values[f.key] || '#ffffff', oninput: () => set(f.key, control.value) });
        break;
      case 'path': {
        const input = h('input', { type: 'text', value: values[f.key] ?? '', placeholder: f.placeholder || '', spellcheck: false, oninput: () => set(f.key, input.value) });
        const browse = async () => {
          const api = ctx.api;
          let picked = null;
          if (f.mode === 'folder') picked = await api.pickFolder(f.label || 'Choose folder');
          else picked = (await api.pickFiles(f.label || 'Choose file', f.filters || [], false))[0];
          if (picked) { input.value = picked; set(f.key, picked); }
        };
        const clear = () => { input.value = ''; set(f.key, ''); };
        control = h('div', { class: 'path-input' }, input,
          h('button', { class: 'btn small', type: 'button', onclick: browse }, 'Browse'),
          h('button', { class: 'btn ghost small icon-only', type: 'button', title: 'Clear', onclick: clear }, icon('x')));
        control.setValue = (v) => { input.value = v; set(f.key, v); };
        break;
      }
      case 'custom': {
        // f.render(values, set, ctx) returns an element; call set(key, value) to change a value
        return h('div', { class: 'field' }, label, f.render(values, set, ctx), hint);
      }
      case 'row': {
        const row = h('div', { class: 'field-row' });
        f.children.forEach((c) => { const el = build(c); row.append(el); entries.push({ f: c, el }); });
        return h('div', { class: 'field' }, label, row, hint);
      }
      default:
        return h('div', {}, `unknown field ${f.type}`);
    }
    const wrap = h('div', { class: 'field' }, label, control, hint);
    wrap.control = control;
    return wrap;
  };

  for (const f of fields) {
    const el = build(f);
    entries.push({ f, el });
    root.append(el);
  }
  function refresh() {
    for (const { f, el } of entries) el.hidden = f.show ? !f.show(values, ctx) : false;
  }
  refresh();
  const byKey = Object.fromEntries(entries.filter((e) => e.f.key).map((e) => [e.f.key, e.el]));
  return { refresh, byKey };
}
