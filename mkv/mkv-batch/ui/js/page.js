// A tool page: header, file queue, options panel and the run bar.
import { api } from './api.js';
import { h, icon, toast, renderFields, fmtTime } from './ui.js';
import { Queue } from './queue.js';

const FINAL = new Set(['done', 'warn', 'skipped', 'error', 'cancelled']);

const store = {
  load(id, defaults) {
    try { return { ...defaults, ...JSON.parse(localStorage.getItem(`mkvbatch.opts.${id}`) || '{}') }; }
    catch { return { ...defaults }; }
  },
  save(id, values) {
    try { localStorage.setItem(`mkvbatch.opts.${id}`, JSON.stringify(values)); } catch { /* storage full or blocked */ }
  },
};

function allFields(fields) {
  return fields.flatMap((f) => (f.type === 'row' ? allFields(f.children) : [f]));
}

function defaultFor(f) {
  if (f.default !== undefined) return f.default;
  if (f.type === 'check') return false;
  if (f.type === 'number' || f.type === 'range') return 0;
  if ((f.type === 'select' || f.type === 'segmented') && Array.isArray(f.options)) return f.options[0][0];
  return '';
}

export class ToolPage {
  constructor(tool, ctx) {
    this.tool = tool;
    this.ctx = ctx;
    this.job = null;
    this.timer = null;
    const defaults = Object.fromEntries(allFields(tool.fields).filter((f) => f.key).map((f) => [f.key, defaultFor(f)]));
    this.values = store.load(tool.id, defaults);
    this.queue = new Queue({
      accept: tool.accept,
      acceptLabel: tool.acceptLabel,
      onFocus: (item) => tool.onFocus?.(item, this),
      onChange: () => { tool.onQueueChange?.(this); this.updateRunbar(); },
      excludeMkvOption: tool.excludeMkvOption,
    });
    this.el = this.build();
    this.queue.render();
    tool.init?.(this);
    this.updateRunbar();
  }

  build() {
    const tool = this.tool;
    this.reqChip = h('button', { class: 'chip', type: 'button', hidden: true, onclick: () => this.ctx.show('settings') });
    const head = h('header', { class: 'page-head' },
      h('div', {},
        h('div', { class: 'eyebrow' }, tool.group),
        h('h1', {}, tool.title),
        h('p', {}, tool.blurb)),
      h('div', { class: 'head-meta' }, this.reqChip));

    this.fieldsRoot = h('div', { class: 'fields' });
    this.renderForm();
    const side = tool.side ? tool.side(this) : null;
    const main = tool.main ? tool.main(this) : null;

    this.startBtn = h('button', { class: 'btn primary', type: 'button', onclick: () => this.start() }, icon('play'), tool.startLabel || 'Start');
    this.pauseBtn = h('button', { class: 'btn', type: 'button', disabled: true, onclick: () => this.togglePause() });
    this.paintPause(false);
    this.cancelBtn = h('button', { class: 'btn', type: 'button', disabled: true, onclick: () => this.cancel() }, icon('stop'), 'Cancel');
    this.meter = h('span');
    this.runText = h('span', { class: 'run-text' });
    this.runCounts = h('span', { class: 'run-counts' });

    return h('section', { class: 'page', 'data-tool': tool.id, hidden: true },
      head,
      h('div', { class: 'page-body' },
        h('div', { class: 'work' }, this.queue.el, main),
        h('aside', { class: 'card options' }, h('div', { class: 'options-title' }, 'Options'), this.fieldsRoot, side)),
      h('footer', { class: 'runbar' }, this.startBtn, this.pauseBtn, this.cancelBtn,
        h('div', { class: 'run-info' }, h('div', { class: 'run-line' }, this.runText, this.runCounts), h('div', { class: 'meter' }, this.meter))));
  }

  renderForm() {
    this.fieldsRoot.replaceChildren();
    this.form = renderFields(this.fieldsRoot, this.tool.fields, this.values, (key, value) => {
      store.save(this.tool.id, this.values);
      this.tool.onValues?.(this, key, value);
      this.updateRunbar();
    }, { api, langs: this.ctx.langs, page: this });
  }

  /** Changes option values from code (e.g. a dropped file) and redraws the form. */
  setValues(patch) {
    Object.assign(this.values, patch);
    store.save(this.tool.id, this.values);
    this.renderForm();
    this.tool.onValues?.(this, Object.keys(patch)[0], Object.values(patch)[0]);
  }

  setToolStatus(status) {
    const need = this.tool.requires;
    if (!need) return;
    const t = status.find((s) => s.id === need);
    const names = { mkvtoolnix: 'MKVToolNix', ffmpeg: 'ffmpeg' };
    const ok = !!t?.path;
    const version = t?.version?.match(/v?(\d+(\.\d+)+)/)?.[1];
    this.reqChip.hidden = false;
    this.reqChip.className = `chip ${ok ? 'ok' : 'bad'}`;
    this.reqChip.textContent = ok ? `${names[need]} ${version || ''}`.trim() : `${names[need]} not found · open Settings`;
    this.reqChip.title = t?.path || 'Set the program location in Settings';
  }

  async handleDrop(paths) {
    let rest = paths;
    if (this.tool.onDrop) rest = await this.tool.onDrop(paths, this);
    if (rest && rest.length) {
      const n = await this.queue.addPaths(rest, true);
      if (n) toast(`${n} file${n === 1 ? '' : 's'} added`, 'ok', 1800);
    }
  }

  async start() {
    if (this.job) return;
    const q = this.queue;
    if (!q.items.length) { toast('Add some files first.', 'info'); return; }
    const idx = q.runnable();
    if (!idx.length) { toast('Everything in the list is finished. Use Re-queue to run it again.', 'info'); return; }
    const problem = this.tool.validate?.(this.values, this);
    if (problem) { toast(problem, 'error'); return; }
    if (this.tool.beforeStart && (await this.tool.beforeStart(this)) === false) return;

    const options = this.tool.collect ? this.tool.collect(this.values, this) : { ...this.values };
    idx.forEach((i) => { Object.assign(q.items[i], { status: 'queued', progress: 0, message: '' }); q.update(i); });
    this.job = { id: null, map: idx, started: Date.now(), paused: false, pausedAt: 0, pausedMs: 0 };
    q.setRunning(true);
    this.setRunning(true);
    try {
      const id = await api.startJob(this.tool.job, idx.map((i) => q.items[i].path), options);
      this.job.id = id;
      this.ctx.registerJob(id, this);
    } catch (e) {
      toast(String(e), 'error');
      this.finish(null);
    }
  }

  /** Freezes the running tools and holds back the remaining files; elapsed time stops too. */
  async togglePause() {
    const job = this.job;
    if (!job?.id) return;
    const on = !job.paused;
    try { await api.pauseJob(job.id, on); } catch (e) { toast(String(e), 'error'); return; }
    job.paused = on;
    if (on) job.pausedAt = Date.now();
    else { job.pausedMs += Date.now() - job.pausedAt; job.pausedAt = 0; }
    this.paintPause(on);
    this.el.classList.toggle('paused', on);
    this.updateRunbar();
  }

  paintPause(paused) {
    this.pauseBtn.replaceChildren(icon(paused ? 'play' : 'pause'), paused ? 'Resume' : 'Pause');
    this.pauseBtn.title = paused ? 'Continue the job' : 'Pause the job (running tools are frozen, nothing is lost)';
  }

  elapsed(job) {
    return Date.now() - job.started - job.pausedMs - (job.pausedAt ? Date.now() - job.pausedAt : 0);
  }

  cancel() {
    if (!this.job?.id) return;
    api.cancelJob(this.job.id);
    this.pauseBtn.disabled = true;
    this.cancelBtn.disabled = true;
    this.runText.textContent = 'Cancelling…';
  }

  onJobEvent(ev) {
    if (ev.type === 'done') { this.finish(ev); return; }
    if (ev.type !== 'file' || !this.job) return;
    const qi = this.job.map[ev.index];
    const item = this.queue.items[qi];
    if (!item) return;
    item.status = ev.status;
    item.progress = ev.progress;
    if (ev.status !== 'running' || ev.message) item.message = ev.message;
    this.queue.update(qi);
    this.updateRunbar();
  }

  finish(ev) {
    const job = this.job;
    this.job = null;
    if (job) {
      for (const qi of job.map) {
        const it = this.queue.items[qi];
        if (it && !FINAL.has(it.status)) {
          it.status = ev?.cancelled ? 'cancelled' : 'queued';
          it.progress = 0;
          this.queue.update(qi);
        }
      }
    }
    this.queue.setRunning(false);
    this.setRunning(false);
    if (ev && job) {
      const parts = [`${ev.ok} done`];
      if (ev.failed) parts.push(`${ev.failed} failed`);
      if (ev.skipped) parts.push(`${ev.skipped} skipped`);
      const kind = ev.failed ? 'error' : ev.cancelled ? 'info' : 'ok';
      toast(`${this.tool.title}: ${ev.cancelled ? 'cancelled · ' : ''}${parts.join(' · ')} in ${fmtTime(this.elapsed(job))}`, kind, 7000);
    }
    this.tool.afterJob?.(this);
    if (ev && job && this.ctx.settings.clearAfterFinish !== false) this.queue.clearFinished();
    this.updateRunbar();
  }

  setRunning(v) {
    this.startBtn.disabled = v;
    this.cancelBtn.disabled = !v;
    this.pauseBtn.disabled = !v;
    this.paintPause(false);
    this.el.classList.toggle('running', v);
    this.el.classList.remove('paused');
    this.ctx.markRunning(this.tool.id, v);
    clearInterval(this.timer);
    if (v) this.timer = setInterval(() => this.updateRunbar(), 1000);
  }

  updateRunbar() {
    const q = this.queue;
    const c = q.counts();
    if (this.job) {
      const items = this.job.map.map((i) => q.items[i]).filter(Boolean);
      const pct = items.reduce((s, it) => s + (FINAL.has(it.status) ? 100 : it.status === 'running' ? it.progress : 0), 0) / Math.max(1, items.length);
      const finished = items.filter((it) => FINAL.has(it.status)).length;
      const running = items.filter((it) => it.status === 'running');
      const current = running.length === 1 ? running[0].name : running.length ? `${running.length} files in parallel` : 'starting…';
      this.meter.style.width = `${pct.toFixed(1)}%`;
      const state = this.job.paused ? 'Paused · ' : '';
      this.runText.textContent = `${state}${finished} of ${items.length} · ${current} · ${fmtTime(this.elapsed(this.job))}`;
    } else {
      this.meter.style.width = '0%';
      const n = q.runnable().length;
      this.runText.textContent = q.items.length ? `Ready · ${n} file${n === 1 ? '' : 's'} to process` : 'Add files to begin';
    }
    const counts = [['done', c.done + c.warn, 'ok'], ['failed', c.error, 'err'], ['skipped', c.skipped, 'muted']]
      .filter(([, n]) => n)
      .map(([label, n, k]) => h('span', { class: `cnt ${k}` }, `${n} ${label}`));
    this.runCounts.replaceChildren(...counts);
  }
}
