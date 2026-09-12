// App bootstrap: navigation, job event routing, drag & drop, activity log, theme.
import { api, listen, appWindow } from './api.js';
import { h, icon, toast, confirmDialog, hydrateIcons } from './ui.js';
import { TOOLS } from './tools.js';
import { ToolPage } from './page.js';
import { SettingsPage } from './settings.js';

const ctx = {
  settings: null,
  langs: [],
  toolStatus: [],
  pages: {},
  jobs: new Map(),
  pending: new Map(),
  active: null,

  async saveSettings() {
    try { await api.saveSettings(ctx.settings); }
    catch (e) { toast(`Could not save settings: ${e}`, 'error'); }
  },

  registerJob(id, page) {
    ctx.jobs.set(id, page);
    const early = ctx.pending.get(id);
    if (early) { ctx.pending.delete(id); early.forEach(route); }
  },

  markRunning(id, on) {
    document.querySelector(`.nav-item[data-id="${id}"]`)?.classList.toggle('running', on);
  },

  async refreshTools() {
    try { ctx.toolStatus = await api.toolStatus(); } catch { ctx.toolStatus = []; }
    Object.values(ctx.pages).forEach((p) => p.setToolStatus?.(ctx.toolStatus));
    renderToolDots();
  },

  show(id) {
    if (!ctx.pages[id]) id = 'remux';
    ctx.active = id;
    Object.entries(ctx.pages).forEach(([pid, p]) => { p.el.hidden = pid !== id; });
    document.querySelectorAll('.nav-item').forEach((n) => n.classList.toggle('active', n.dataset.id === id));
    try { localStorage.setItem('mkvbatch.page', id); } catch { /* ignore */ }
  },

  applyTheme(theme) {
    document.documentElement.dataset.theme = theme === 'light' ? 'light' : 'dark';
    appWindow().setTheme(theme === 'light' ? 'light' : 'dark').catch(() => {});
  },
};

// --- job events -------------------------------------------------------------
function route(ev) {
  if (ev.type === 'log') {
    const kind = ev.job.split('-')[0];
    addLog(ev.level, TOOLS.find((t) => t.job === kind)?.label || kind, ev.text);
    return;
  }
  const page = ctx.jobs.get(ev.job);
  if (!page) {
    // events can arrive before start_job returned the id
    const list = ctx.pending.get(ev.job) || [];
    list.push(ev);
    ctx.pending.set(ev.job, list);
    return;
  }
  page.onJobEvent(ev);
  if (ev.type === 'done') ctx.jobs.delete(ev.job);
}

// --- activity log -------------------------------------------------------------
const log = { panel: null, body: null, badge: null, errors: 0, lines: [] };

function addLog(level, source, text) {
  const time = new Date().toLocaleTimeString([], { hour12: false });
  log.lines.push(`${time} [${level}] ${source}: ${text}`);
  if (log.lines.length > 3000) { log.lines.shift(); log.body.firstChild?.remove(); }
  const line = h('div', { class: `log-line lv-${level}` }, h('span', { class: 'log-time' }, time), h('span', { class: 'log-src' }, source), h('span', { class: 'log-text' }, text));
  const stick = log.body.scrollTop + log.body.clientHeight >= log.body.scrollHeight - 20;
  log.body.append(line);
  if (stick) log.body.scrollTop = log.body.scrollHeight;
  if (level === 'error' && log.panel.hidden) {
    log.errors++;
    log.badge.hidden = false;
    log.badge.textContent = String(log.errors);
  }
}

function setupLog() {
  log.panel = document.getElementById('logPanel');
  log.body = document.getElementById('logBody');
  log.badge = document.getElementById('logBadge');
  const showCmd = document.getElementById('logShowCmd');
  const applyCmd = () => log.body.classList.toggle('hide-cmd', !showCmd.checked);
  showCmd.onchange = applyCmd;
  applyCmd();
  const toggle = (open = log.panel.hidden) => {
    log.panel.hidden = !open;
    if (open) { log.errors = 0; log.badge.hidden = true; log.body.scrollTop = log.body.scrollHeight; }
  };
  document.getElementById('logToggle').onclick = () => toggle();
  document.getElementById('logClose').onclick = () => toggle(false);
  document.getElementById('logClear').onclick = () => { log.lines = []; log.body.replaceChildren(); };
  document.getElementById('logCopy').onclick = async () => {
    try { await navigator.clipboard.writeText(log.lines.join('\n')); toast('Log copied', 'ok', 1500); }
    catch { toast('Could not copy the log', 'error'); }
  };
  ctx.toggleLog = toggle;
}

// --- sidebar ------------------------------------------------------------------------
function buildNav() {
  const nav = document.getElementById('nav');
  const groups = [...new Set(TOOLS.map((t) => t.group))];
  for (const g of groups) {
    nav.append(h('div', { class: 'nav-group' }, g));
    TOOLS.filter((t) => t.group === g).forEach((t) => nav.append(navItem(t.id, t.label, t.icon)));
  }
  nav.append(h('div', { class: 'nav-spacer' }), navItem('settings', 'Settings', 'settings'));
  const sameDir = h('input', {
    type: 'checkbox',
    checked: !!ctx.settings.backupSameDir,
    onchange: async () => {
      ctx.settings.backupSameDir = sameDir.checked;
      await ctx.saveSettings();
    },
  });
  document.getElementById('backupLocationControl').replaceChildren(
    h('label', { class: 'check small', title: 'Choose where replaced originals are backed up' },
      sameDir, h('span', {}, 'backup in same directory')),
  );
}

function navItem(id, label, iconName) {
  return h('button', { class: 'nav-item', type: 'button', 'data-id': id, onclick: () => ctx.show(id) },
    icon(iconName), h('span', { class: 'nav-label' }, label), h('span', { class: 'run-dot', title: 'Running' }));
}

function renderToolDots() {
  const names = { mkvtoolnix: 'MKVToolNix', ffmpeg: 'ffmpeg' };
  document.getElementById('toolDots').replaceChildren(...ctx.toolStatus.map((t) =>
    h('button', { class: `tool-dot ${t.path ? 'ok' : 'bad'}`, type: 'button', title: t.version || 'Not found, click to open Settings', onclick: () => ctx.show('settings') },
      h('i'), names[t.id])));
}

// --- drag & drop ------------------------------------------------------------------------
function setupDrop() {
  const overlay = document.getElementById('dropOverlay');
  const text = document.getElementById('dropText');
  const target = () => { const p = ctx.pages[ctx.active]; return p?.handleDrop ? p : null; };
  listen('tauri://drag-enter', () => {
    const p = target();
    if (!p || p.queue?.running) return;
    text.textContent = `Drop to add to ${p.tool.title}`;
    overlay.hidden = false;
  });
  listen('tauri://drag-leave', () => { overlay.hidden = true; });
  listen('tauri://drag-drop', (e) => {
    overlay.hidden = true;
    const p = target();
    const paths = e.payload?.paths || [];
    if (p && paths.length) p.handleDrop(paths);
  });
}

// --- keyboard -------------------------------------------------------------------------------
function setupKeys() {
  document.addEventListener('keydown', (e) => {
    const p = ctx.pages[ctx.active];
    if (e.ctrlKey && e.key.toLowerCase() === 'o' && p?.queue) { e.preventDefault(); p.queue.browseFiles(); }
    if (e.ctrlKey && e.key === 'Enter' && p?.start) { e.preventDefault(); p.start(); }
    if (e.ctrlKey && e.key.toLowerCase() === 'l') { e.preventDefault(); ctx.toggleLog(); }
    if (e.key === 'Escape') document.querySelector('.modal-overlay')?.click();
  });
}

async function init() {
  hydrateIcons();
  [ctx.settings, ctx.langs] = await Promise.all([api.settings(), api.languages()]);
  ctx.applyTheme(ctx.settings.theme);
  buildNav();
  setupLog();

  const pagesRoot = document.getElementById('pages');
  for (const tool of TOOLS) {
    const page = new ToolPage(tool, ctx);
    ctx.pages[tool.id] = page;
    pagesRoot.append(page.el);
  }
  ctx.pages.settings = new SettingsPage(ctx);
  pagesRoot.append(ctx.pages.settings.el);

  let last = 'remux';
  try { last = localStorage.getItem('mkvbatch.page') || 'remux'; } catch { /* ignore */ }
  ctx.show(last);

  await listen('job', (e) => route(e.payload));
  await listen('confirm-close', async () => {
    const ok = await confirmDialog({
      title: 'Jobs are still running',
      text: 'Quitting cancels them. Files being written are discarded, your originals are not touched.',
      ok: 'Cancel jobs and quit', cancel: 'Keep working', danger: true,
    });
    if (ok) api.forceQuit();
  });
  setupDrop();
  setupKeys();
  ctx.refreshTools();
}

init().catch((e) => {
  document.body.append(h('pre', { class: 'fatal' }, `MKV Batch failed to start:\n${e?.stack || e}`));
});
