// File queue: the list of files a tool will process, with per-file status and progress.
import { api } from './api.js';
import { h, icon, fmtSize, toast } from './ui.js';

const STATUS_LABEL = {
  queued: 'Queued', running: 'Working', done: 'Done', warn: 'Done', error: 'Failed',
  skipped: 'Skipped', cancelled: 'Cancelled',
};
const FINISHED = new Set(['done', 'warn', 'skipped']);

export class Queue {
  /**
   * @param {object} o
   * @param {string[]} o.accept   accepted extensions (without dot)
   * @param {string}   o.acceptLabel text shown in the empty state
   * @param {Function} o.onFocus  (item) when a row is clicked
   * @param {Function} o.onChange () when items are added/removed
   */
  constructor({ accept, acceptLabel, onFocus, onChange, excludeMkvOption }) {
    this.accept = accept;
    this.items = [];
    /** lower-cased paths already listed, so the same file is never queued twice */
    this.known = new Set();
    /** folder scans still in progress */
    this.scanning = 0;
    this.focus = -1;
    this.running = false;
    this.onFocus = onFocus || (() => {});
    this.onChange = onChange || (() => {});
    this.recursive = true;
    this.excludeMkvOption = !!excludeMkvOption;
    this.excludeMkv = this.excludeMkvOption;
    this.el = this.build(acceptLabel);
  }

  build(acceptLabel) {
    this.btnAdd = h('button', { class: 'btn small', type: 'button', onclick: () => this.browseFiles() }, icon('plus'), 'Add files');
    this.btnFolder = h('button', { class: 'btn small', type: 'button', onclick: () => this.browseFolder() }, icon('folder'), 'Add folder');
    const rec = h('input', { type: 'checkbox', class: 'toggle', checked: true, onchange: () => { this.recursive = rec.checked; } });
    const excludeMkv = h('input', { type: 'checkbox', class: 'toggle', checked: true, onchange: () => { this.excludeMkv = excludeMkv.checked; } });
    const excludeMkvLabel = this.excludeMkvOption
      ? h('label', { class: 'check small exclude-mkv', title: 'Skip MKV files when adding a folder' }, excludeMkv, h('span', {}, 'exclude MKV'))
      : null;
    // labels hide on narrow queues (see .bt in app.css); the title keeps them discoverable
    const tool = (ico, text, title, onclick) =>
      h('button', { class: 'btn ghost small', type: 'button', title, onclick }, icon(ico), h('span', { class: 'bt' }, text));
    this.btnRemove = tool('trash', 'Remove', 'Remove the ticked (or highlighted) files  [Del]', () => this.removeSelected());
    this.btnReset = tool('reset', 'Re-queue', 'Mark finished files as queued again', () => this.resetStatus());
    this.btnSweep = tool('sweep', 'Clear done', 'Remove finished files from the list', () => this.clearFinished());
    this.btnClear = tool('x', 'Clear', 'Remove all files from the list', () => this.clear());

    this.checkAll = h('input', { type: 'checkbox', title: 'Select all', onchange: () => this.setAllChecked(this.checkAll.checked) });
    this.body = h('div', { class: 'q-body', tabindex: 0 });
    this.body.addEventListener('keydown', (e) => {
      if (e.key === 'Delete') { e.preventDefault(); this.removeSelected(); }
      if (e.key === 'a' && e.ctrlKey) { e.preventDefault(); this.setAllChecked(true); }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        const next = Math.max(0, Math.min(this.items.length - 1, this.focus + (e.key === 'ArrowDown' ? 1 : -1)));
        this.setFocus(next, true);
      }
    });
    this.empty = h('div', { class: 'q-empty' },
      h('div', { class: 'q-empty-inner' },
        icon('plus', 'ico big'),
        h('div', { class: 'q-empty-title' }, 'Drop files or folders here'),
        h('div', { class: 'q-empty-sub' }, acceptLabel || ''),
        h('div', { class: 'q-empty-actions' },
          h('button', { class: 'btn small', type: 'button', onclick: () => this.browseFiles() }, 'Browse files'),
          h('button', { class: 'btn small', type: 'button', onclick: () => this.browseFolder() }, 'Browse folder'))));
    this.countEl = h('span', { class: 'q-count' });

    return h('div', { class: 'card queue' },
      h('div', { class: 'q-toolbar' }, this.btnAdd, this.btnFolder,
        h('label', { class: 'check small subfolders', title: 'Include files in subfolders when adding a folder' }, rec, h('span', {}, 'subfolders')),
        excludeMkvLabel,
        h('span', { class: 'grow' }), this.countEl, this.btnRemove, this.btnReset, this.btnSweep, this.btnClear),
      h('div', { class: 'q-head' }, h('span', {}, this.checkAll), h('span', {}, 'File'), h('span', { class: 'right' }, 'Size'), h('span', {}, 'Status'), h('span', {})),
      this.body, this.empty);
  }

  async browseFiles() {
    const exts = this.accept;
    const paths = await api.pickFiles('Add files', exts.length ? [{ name: 'Supported files', extensions: exts }, { name: 'All files', extensions: ['*'] }] : []);
    if (paths.length) await this.addPaths(paths, false);
  }

  async browseFolder() {
    const dir = await api.pickFolder('Add a folder');
    if (dir) await this.addPaths([dir], this.recursive);
  }

  /** Files are listed as the scan finds them, then put in natural order once it completes. */
  async addPaths(paths, recursive = true) {
    if (this.running) { toast('Wait for the current job to finish before adding files.', 'info'); return 0; }
    const keep = (list) => (recursive && this.excludeMkv ? list.filter((e) => e.ext !== 'mkv') : list);
    const mine = new Set();
    let found = 0;
    this.scanning++;
    this.updateCount();
    try {
      const all = await api.scan(paths, this.accept, recursive, (batch) => {
        const entries = keep(batch);
        found += entries.length;
        this.add(entries).forEach((it) => mine.add(it));
      });
      this.add(keep(all)).forEach((it) => mine.add(it));
      this.sortAdded(mine, keep(all));
    } catch (e) {
      toast(`Could not read ${paths.length === 1 ? paths[0] : 'those folders'}: ${e}`, 'error');
    } finally {
      this.scanning--;
      this.updateCount();
    }
    if (!mine.size) toast(found ? 'Those files are already in the list.' : 'No supported files found.', 'info');
    return mine.size;
  }

  /** Appends entries whose path isn't listed yet; returns the new items. */
  add(entries) {
    const fresh = [];
    for (const e of entries) {
      const key = e.path.toLowerCase();
      if (this.known.has(key)) continue;
      this.known.add(key);
      const item = { ...e, status: 'queued', progress: 0, message: '', note: '', checked: false };
      this.items.push(item);
      fresh.push(item);
    }
    if (fresh.length) {
      const start = this.items.length - fresh.length;
      this.body.append(...fresh.map((it, k) => this.rowEl(it, start + k)));
      this.showEmpty();
      this.updateCount();
      this.onChange();
    }
    if (this.focus < 0 && this.items.length) this.setFocus(0);
    return fresh;
  }

  /** Reorders the items one scan added (they arrive folder by folder) to match the sorted scan result. */
  sortAdded(mine, sorted) {
    if (!mine.size || this.running) return;
    const rank = new Map(sorted.map((e, i) => [e.path.toLowerCase(), i]));
    const slots = [];
    this.items.forEach((it, i) => { if (mine.has(it)) slots.push(i); });
    const ordered = slots.map((i) => this.items[i]).sort((a, b) => rank.get(a.path.toLowerCase()) - rank.get(b.path.toLowerCase()));
    if (ordered.every((it, k) => this.items[slots[k]] === it)) return;
    const focused = this.items[this.focus];
    slots.forEach((i, k) => { this.items[i] = ordered[k]; });
    this.focus = focused ? this.items.indexOf(focused) : -1;
    this.render();
  }

  remove(indices) {
    const drop = new Set(indices);
    const focused = this.items[this.focus];
    this.items = this.items.filter((_, i) => !drop.has(i));
    this.known = new Set(this.items.map((it) => it.path.toLowerCase()));
    this.focus = focused ? this.items.indexOf(focused) : -1;
    this.render();
    this.onChange();
    if (this.focus < 0 && this.items.length) this.setFocus(0);
    if (!this.items.length) this.onFocus(null);
  }

  removeSelected() {
    if (this.running) return;
    const checked = this.checkedIndices();
    if (checked.length) this.remove(checked);
    else if (this.focus >= 0) this.remove([this.focus]);
  }

  clear() { if (!this.running) this.remove(this.items.map((_, i) => i)); }

  clearFinished() {
    if (this.running) return;
    this.remove(this.items.map((it, i) => (FINISHED.has(it.status) ? i : -1)).filter((i) => i >= 0));
  }

  resetStatus() {
    if (this.running) return;
    this.items.forEach((it) => { if (it.status !== 'queued') { it.status = 'queued'; it.progress = 0; it.message = ''; } });
    this.render();
  }

  checkedIndices() { return this.items.map((it, i) => (it.checked ? i : -1)).filter((i) => i >= 0); }

  setAllChecked(v) {
    this.items.forEach((it) => { it.checked = v; });
    this.render();
  }

  /** Files that Start will process: the ticked ones, or everything not finished yet. */
  runnable() {
    const checked = this.checkedIndices();
    if (checked.length) return checked;
    return this.items.map((it, i) => (FINISHED.has(it.status) ? -1 : i)).filter((i) => i >= 0);
  }

  setFocus(i, scroll = false) {
    if (i < 0 || i >= this.items.length) return;
    const prev = this.body.querySelector('.q-row.focus');
    if (prev) prev.classList.remove('focus');
    this.focus = i;
    const row = this.body.children[i];
    if (row) { row.classList.add('focus'); if (scroll) row.scrollIntoView({ block: 'nearest' }); }
    this.onFocus(this.items[i]);
  }

  setRunning(v) {
    this.running = v;
    [this.btnAdd, this.btnFolder, this.btnRemove, this.btnReset, this.btnSweep, this.btnClear].forEach((b) => { b.disabled = v; });
    this.el.classList.toggle('is-running', v);
  }

  counts() {
    const c = { total: this.items.length, done: 0, warn: 0, error: 0, skipped: 0 };
    this.items.forEach((it) => { if (c[it.status] !== undefined) c[it.status]++; });
    return c;
  }

  rowEl(item, i) {
    const check = h('input', { type: 'checkbox', checked: item.checked, onchange: () => { item.checked = check.checked; this.updateCount(); } });
    check.addEventListener('click', (e) => e.stopPropagation());
    const row = h('div', { class: `q-row st-row-${item.status}${i === this.focus ? ' focus' : ''}`, onclick: () => this.setFocus(i), ondblclick: () => api.reveal(item.path) },
      h('label', { class: 'q-check' }, check),
      h('div', { class: 'q-name' }, h('div', { class: 'q-file', title: item.path }, item.name), h('div', { class: 'q-dir', title: item.dir }, item.dir)),
      h('div', { class: 'q-size' }, fmtSize(item.size)),
      h('div', { class: 'q-status' }),
      h('button', { class: 'btn ghost small icon-only q-open', type: 'button', title: 'Show in Explorer', onclick: (e) => { e.stopPropagation(); api.reveal(item.path); } }, icon('open')));
    this.paintStatus(row, item);
    return row;
  }

  paintStatus(row, item) {
    const cell = row.querySelector('.q-status');
    const text = item.message || (item.status === 'queued' ? item.note : '');
    const pill = h('span', { class: `pill st-${item.status}` }, item.status === 'running' ? `${Math.round(item.progress)}%` : STATUS_LABEL[item.status] || item.status);
    const parts = [h('div', { class: 'q-status-line' }, pill, h('span', { class: 'q-msg', title: text || '' }, text || ''))];
    if (item.status === 'running') parts.push(h('div', { class: 'q-bar' }, h('span', { style: { width: `${item.progress}%` } })));
    cell.replaceChildren(...parts);
    row.className = `q-row st-row-${item.status}${this.items.indexOf(item) === this.focus ? ' focus' : ''}`;
  }

  update(i) {
    const row = this.body.children[i];
    if (row) this.paintStatus(row, this.items[i]);
  }

  updateCount() {
    const checked = this.checkedIndices().length;
    const n = this.items.length;
    const text = n ? (checked ? `${checked} of ${n} selected` : `${n} file${n === 1 ? '' : 's'}`) : '';
    this.countEl.textContent = this.scanning ? `Scanning… ${text}`.trim() : text;
    this.countEl.classList.toggle('scanning', this.scanning > 0);
    this.checkAll.checked = this.items.length > 0 && checked === this.items.length;
    this.checkAll.indeterminate = checked > 0 && checked < this.items.length;
  }

  render() {
    this.body.replaceChildren(...this.items.map((it, i) => this.rowEl(it, i)));
    this.showEmpty();
    this.updateCount();
  }

  showEmpty() {
    const empty = this.items.length === 0;
    this.empty.hidden = !empty;
    this.body.hidden = empty;
  }
}
