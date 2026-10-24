// File queue: the list of files a tool will process, with per-file status and progress.
import { api } from './api.js';
import { h, icon, fmtSize, toast } from './ui.js';
import { EXT } from './tools.js';

const STATUS_LABEL = {
  queued: 'Queued', running: 'Working', done: 'Done', warn: 'Done', error: 'Failed',
  skipped: 'Skipped', cancelled: 'Cancelled',
};
const FINISHED = new Set(['done', 'warn', 'skipped']);

function parseFilterTokens(str) {
  if (!str) return [];
  return str
    .split(/[,;\s]+/)
    .map((t) => t.trim().toLowerCase())
    .filter(Boolean);
}

function matchExtOnly(ext, tokens) {
  const e = (ext || '').toLowerCase();
  for (const t of tokens) {
    const clean = t.startsWith('.') ? t.slice(1) : t;
    if (clean === e) return true;
    if (t.startsWith('*.') && t.slice(2) === e) return true;
  }
  return false;
}

function matchEntry(entry, tokens) {
  if (!tokens || !tokens.length) return false;
  const name = (entry.name || '').toLowerCase();
  const ext = (entry.ext || '').toLowerCase();

  for (const token of tokens) {
    if (token.includes('*') || token.includes('?')) {
      const regexStr = '^' + token
        .replace(/[-/\\^$+?.()|[\]{}]/g, '\\$&')
        .replace(/\\\*/g, '.*')
        .replace(/\\\?/g, '.') + '$';
      try {
        const re = new RegExp(regexStr, 'i');
        if (re.test(name) || re.test(ext) || re.test('.' + ext)) return true;
      } catch {
        if (name.includes(token)) return true;
      }
    } else {
      const clean = token.startsWith('.') ? token.slice(1) : token;
      if (clean && ext === clean) return true;
      if (name === token || name.includes(token)) return true;
    }
  }
  return false;
}

export class Queue {
  /**
   * @param {object} o
   * @param {string[]} o.accept   accepted extensions (without dot)
   * @param {string}   o.acceptLabel text shown in the empty state
   * @param {Function} o.onFocus  (item) when a row is clicked
   * @param {Function} o.onChange () when items are added/removed
   */
  constructor({ accept, acceptLabel, onFocus, onChange, excludeMkvOption, excludeVideoOption, fileFilterOption }) {
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
    this.excludeVideoOption = !!excludeVideoOption;
    this.excludeVideo = this.excludeVideoOption;
    this.fileFilterOption = !!fileFilterOption;
    this.filterInclude = '';
    this.filterExclude = '';
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
    const excludeVideo = h('input', { type: 'checkbox', class: 'toggle', checked: true, onchange: () => { this.excludeVideo = excludeVideo.checked; } });
    const excludeVideoLabel = this.excludeVideoOption
      ? h('label', { class: 'check small exclude-video', title: 'Exclude video files when importing' }, excludeVideo, h('span', {}, 'exclude videos'))
      : null;

    this.filterDot = h('span', { class: 'filter-dot', hidden: true });
    this.btnFilter = this.fileFilterOption
      ? h('button', {
          class: 'btn ghost small btn-filter',
          type: 'button',
          title: 'Filter files before importing (specify or exclude)',
          onclick: () => this.toggleFilterBar(),
        }, icon('filter'), h('span', { class: 'bt' }, 'Filter'), this.filterDot)
      : null;

    this.inputInclude = h('input', {
      type: 'text',
      class: 'q-filter-input',
      placeholder: 'all supported, or e.g. mp3, flac, *live*',
      title: 'Only import files matching these extensions or patterns (comma-separated)',
      oninput: (e) => {
        this.filterInclude = e.target.value.trim();
        this.updateFilterState();
      },
    });

    this.inputExclude = h('input', {
      type: 'text',
      class: 'q-filter-input',
      placeholder: 'e.g. wav, *sample*, temp*',
      title: 'Exclude files matching these extensions or patterns (comma-separated)',
      oninput: (e) => {
        this.filterExclude = e.target.value.trim();
        this.updateFilterState();
      },
    });

    this.btnClearFilter = h('button', {
      class: 'btn ghost small btn-filter-clear',
      type: 'button',
      title: 'Clear filter',
      onclick: () => this.clearFilters(),
    }, icon('x'), h('span', { class: 'bt' }, 'Clear'));

    this.filterBar = this.fileFilterOption
      ? h('div', { class: 'q-filter-bar', hidden: true },
          h('div', { class: 'q-filter-col' },
            h('span', { class: 'q-filter-label' }, 'Specify:'),
            this.inputInclude),
          h('div', { class: 'q-filter-col' },
            h('span', { class: 'q-filter-label' }, 'Exclude:'),
            this.inputExclude),
          this.btnClearFilter)
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
    this.scanText = h('span', { class: 'q-scan-text' });
    this.scanEl = h('div', { class: 'q-scan', hidden: true, role: 'status' }, h('span', { class: 'spinner' }), this.scanText);

    return h('div', { class: 'card queue' },
      h('div', { class: 'q-toolbar' }, this.btnAdd, this.btnFolder,
        h('label', { class: 'check small subfolders', title: 'Include files in subfolders when adding a folder' }, rec, h('span', {}, 'subfolders')),
        excludeMkvLabel,
        excludeVideoLabel,
        this.btnFilter,
        h('span', { class: 'grow' }), this.countEl, this.btnRemove, this.btnReset, this.btnSweep, this.btnClear),
      this.filterBar,
      h('div', { class: 'q-head' }, h('span', {}, this.checkAll), h('span', {}, 'File'), h('span', { class: 'right' }, 'Size'), h('span', {}, 'Status'), h('span', {})),
      this.scanEl, this.body, this.empty);
  }

  toggleFilterBar(show) {
    if (!this.filterBar) return;
    const isHidden = typeof show === 'boolean' ? !show : !this.filterBar.hidden;
    this.filterBar.hidden = isHidden;
    if (!isHidden && this.inputInclude) {
      this.inputInclude.focus();
    }
  }

  updateFilterState() {
    const active = !!(this.filterInclude || this.filterExclude);
    if (this.btnFilter) {
      this.btnFilter.classList.toggle('active', active);
      if (this.filterDot) this.filterDot.hidden = !active;
      this.btnFilter.title = active
        ? `Filter active (Specify: ${this.filterInclude || 'all'}, Exclude: ${this.filterExclude || 'none'})`
        : 'Filter files before importing (specify or exclude)';
    }
  }

  clearFilters() {
    this.filterInclude = '';
    this.filterExclude = '';
    if (this.inputInclude) this.inputInclude.value = '';
    if (this.inputExclude) this.inputExclude.value = '';
    this.updateFilterState();
  }

  effectiveAccept() {
    let list = this.accept || [];
    if (this.excludeMkvOption && this.excludeMkv) {
      list = list.filter((e) => e.toLowerCase() !== 'mkv');
    }
    if (this.excludeVideoOption && this.excludeVideo) {
      list = list.filter((e) => !EXT.video.includes(e.toLowerCase()));
    }
    const incTokens = parseFilterTokens(this.filterInclude);
    if (incTokens.length) {
      const matchedExts = list.filter((e) => matchExtOnly(e, incTokens));
      if (matchedExts.length > 0) {
        list = matchedExts;
      }
    }
    return list;
  }

  filterList(list, recursive = true) {
    const incTokens = parseFilterTokens(this.filterInclude);
    const excTokens = parseFilterTokens(this.filterExclude);
    return list.filter((e) => {
      const ext = (e.ext || '').toLowerCase();
      if (this.excludeMkvOption && this.excludeMkv && recursive && ext === 'mkv') {
        return false;
      }
      if (this.excludeVideoOption && this.excludeVideo && EXT.video.includes(ext)) {
        return false;
      }
      if (excTokens.length && matchEntry(e, excTokens)) {
        return false;
      }
      if (incTokens.length && !matchEntry(e, incTokens)) {
        return false;
      }
      return true;
    });
  }

  async browseFiles() {
    const exts = this.effectiveAccept();
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
    const keep = (list) => this.filterList(list, recursive);
    const mine = new Set();
    let found = 0;
    if (!this.scanning++) this.scanFound = 0;
    this.showScan();
    try {
      const all = await api.scan(paths, this.effectiveAccept(), recursive, (batch) => {
        const entries = keep(batch);
        found += entries.length;
        this.scanFound += entries.length;
        this.showScan();
        this.add(entries).forEach((it) => mine.add(it));
      });
      this.add(keep(all)).forEach((it) => mine.add(it));
      this.sortAdded(mine, keep(all));
    } catch (e) {
      toast(`Could not read ${paths.length === 1 ? paths[0] : 'those folders'}: ${e}`, 'error');
    } finally {
      this.scanning--;
      this.showScan();
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
    this.countEl.textContent = text;
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
    this.empty.hidden = !empty || this.scanning > 0;
    this.body.hidden = empty;
    this.scanEl.classList.toggle('alone', empty);
  }

  /** Spinner while folders are being read: centred when the list is still empty, a strip on top otherwise. */
  showScan() {
    this.scanEl.hidden = !this.scanning;
    const n = this.scanFound || 0;
    this.scanText.textContent = n ? `Scanning folders… ${n.toLocaleString()} found` : 'Scanning folders…';
    this.showEmpty();
  }
}
