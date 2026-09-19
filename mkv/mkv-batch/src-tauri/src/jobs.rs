//! Background jobs: one job = one tool run over a list of files.
//! Progress is reported to the UI through the "job" event.

use rayon::prelude::*;
use serde::de::DeserializeOwned;
use serde::Serialize;
use serde_json::Value;
use std::collections::HashMap;
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::path::{Path, PathBuf};
use std::process::Child;
use std::sync::atomic::{AtomicBool, AtomicU64, AtomicUsize, Ordering};
use std::sync::{Arc, Condvar, Mutex};
use std::time::Duration;
use tauri::{AppHandle, Emitter};

pub const CANCELLED: &str = "Cancelled";

/// What happened to one file.
pub enum Outcome {
    Done(String),
    Warn(String),
    Skipped(String),
}

pub type FileResult = Result<Outcome, String>;

#[derive(Default, Clone, Copy)]
pub struct Summary {
    pub ok: usize,
    pub failed: usize,
    pub skipped: usize,
}

#[derive(Serialize, Clone)]
#[serde(tag = "type", rename_all = "camelCase")]
enum JobEvent<'a> {
    File {
        job: &'a str,
        index: usize,
        status: &'a str,
        progress: f32,
        message: &'a str,
    },
    Log {
        job: &'a str,
        level: &'a str,
        text: &'a str,
    },
    Done {
        job: &'a str,
        ok: usize,
        failed: usize,
        skipped: usize,
        cancelled: bool,
    },
}

pub fn parse_opts<T: DeserializeOwned>(value: Value) -> Result<T, String> {
    serde_json::from_value(value).map_err(|e| format!("Invalid options: {e}"))
}

pub struct JobCtx {
    pub id: String,
    app: AppHandle,
    cancelled: AtomicBool,
    paused: Mutex<bool>,
    resumed: Condvar,
    children: Mutex<HashMap<u64, Arc<Mutex<Child>>>>,
    next_child: AtomicU64,
    last_progress: Mutex<HashMap<usize, i32>>,
}

impl JobCtx {
    pub fn is_cancelled(&self) -> bool {
        self.cancelled.load(Ordering::SeqCst)
    }

    pub fn cancel(&self) {
        self.cancelled.store(true, Ordering::SeqCst);
        for child in self.children.lock().unwrap().values() {
            let _ = child.lock().unwrap().kill();
        }
        self.resumed.notify_all();
    }

    /// Pausing freezes running tools (ffmpeg, mkvmerge...) and holds back files not started yet.
    pub fn set_paused(&self, on: bool) {
        let mut paused = self.paused.lock().unwrap();
        if *paused == on {
            return;
        }
        *paused = on;
        for child in self.children.lock().unwrap().values() {
            suspend(&child.lock().unwrap(), on);
        }
        drop(paused);
        self.resumed.notify_all();
    }

    /// Blocks while the job is paused (returns straight away on cancel).
    pub fn wait_if_paused(&self) {
        let mut paused = self.paused.lock().unwrap();
        while *paused && !self.is_cancelled() {
            paused = self.resumed.wait_timeout(paused, Duration::from_millis(250)).unwrap().0;
        }
    }

    pub fn register_child(&self, child: Arc<Mutex<Child>>) -> u64 {
        let key = self.next_child.fetch_add(1, Ordering::SeqCst);
        // hold the pause lock so a pause can't slip in between spawn and registration
        let paused = self.paused.lock().unwrap();
        if *paused {
            suspend(&child.lock().unwrap(), true);
        }
        self.children.lock().unwrap().insert(key, child);
        drop(paused);
        key
    }

    pub fn unregister_child(&self, key: u64) {
        self.children.lock().unwrap().remove(&key);
    }

    pub fn status(&self, index: usize, status: &str, progress: f32, message: &str) {
        let _ = self.app.emit(
            "job",
            JobEvent::File { job: &self.id, index, status, progress, message },
        );
    }

    /// Reports running progress (0-100) for one file; throttled to half-percent steps.
    pub fn progress(&self, index: usize, pct: f32) {
        let pct = pct.clamp(0.0, 100.0);
        let step = (pct * 2.0) as i32;
        {
            let mut last = self.last_progress.lock().unwrap();
            if last.get(&index) == Some(&step) {
                return;
            }
            last.insert(index, step);
        }
        self.status(index, "running", pct, "");
    }

    pub fn log(&self, level: &str, text: &str) {
        let _ = self.app.emit("job", JobEvent::Log { job: &self.id, level, text });
    }

    /// Per-job scratch folder in %TEMP%, removed when the job ends.
    pub fn temp_dir(&self) -> Result<PathBuf, String> {
        let dir = std::env::temp_dir().join("MKVBatch").join(&self.id);
        std::fs::create_dir_all(&dir).map_err(|e| format!("Temp folder: {e}"))?;
        Ok(dir)
    }

    pub fn finish(&self, summary: Summary) {
        let _ = std::fs::remove_dir_all(std::env::temp_dir().join("MKVBatch").join(&self.id));
        let _ = self.app.emit(
            "job",
            JobEvent::Done {
                job: &self.id,
                ok: summary.ok,
                failed: summary.failed,
                skipped: summary.skipped,
                cancelled: self.is_cancelled(),
            },
        );
    }
}

/// Runs `work` for every file (in parallel when `threads > 1`), turning each
/// result into a status event. Panics inside `work` fail only that file.
pub fn run_files<F>(ctx: &JobCtx, files: &[PathBuf], threads: usize, work: F) -> Summary
where
    F: Fn(usize, &Path) -> FileResult + Sync,
{
    let ok = AtomicUsize::new(0);
    let failed = AtomicUsize::new(0);
    let skipped = AtomicUsize::new(0);

    let one = |index: usize, path: &PathBuf| {
        ctx.wait_if_paused();
        if ctx.is_cancelled() {
            ctx.status(index, "cancelled", 0.0, "");
            return;
        }
        ctx.status(index, "running", 0.0, "");
        let name = path
            .file_name()
            .map(|n| n.to_string_lossy().into_owned())
            .unwrap_or_default();
        match catch_unwind(AssertUnwindSafe(|| work(index, path))) {
            Ok(Ok(Outcome::Done(msg))) => {
                ok.fetch_add(1, Ordering::SeqCst);
                ctx.status(index, "done", 100.0, &msg);
            }
            Ok(Ok(Outcome::Warn(msg))) => {
                ok.fetch_add(1, Ordering::SeqCst);
                ctx.status(index, "warn", 100.0, &msg);
                ctx.log("warn", &format!("{name}: {msg}"));
            }
            Ok(Ok(Outcome::Skipped(msg))) => {
                skipped.fetch_add(1, Ordering::SeqCst);
                ctx.status(index, "skipped", 0.0, &msg);
                ctx.log("info", &format!("{name}: skipped, {msg}"));
            }
            Ok(Err(e)) if e == CANCELLED => ctx.status(index, "cancelled", 0.0, ""),
            Ok(Err(e)) => {
                failed.fetch_add(1, Ordering::SeqCst);
                ctx.status(index, "error", 0.0, &e);
                ctx.log("error", &format!("{name}: {e}"));
            }
            Err(_) => {
                failed.fetch_add(1, Ordering::SeqCst);
                ctx.status(index, "error", 0.0, "Internal error");
                ctx.log("error", &format!("{name}: internal error (panic)"));
            }
        }
    };

    let pool = if threads > 1 {
        rayon::ThreadPoolBuilder::new().num_threads(threads).build().ok()
    } else {
        None
    };
    match pool {
        Some(pool) => pool.install(|| {
            files.par_iter().enumerate().for_each(|(i, p)| one(i, p));
        }),
        None => files.iter().enumerate().for_each(|(i, p)| one(i, p)),
    }

    Summary {
        ok: ok.into_inner(),
        failed: failed.into_inner(),
        skipped: skipped.into_inner(),
    }
}

/// Suspends or resumes a whole process (all its threads).
#[cfg(windows)]
fn suspend(child: &Child, on: bool) {
    use std::os::windows::io::AsRawHandle;
    #[link(name = "ntdll")]
    extern "system" {
        fn NtSuspendProcess(process: *mut std::ffi::c_void) -> i32;
        fn NtResumeProcess(process: *mut std::ffi::c_void) -> i32;
    }
    let handle = child.as_raw_handle() as *mut std::ffi::c_void;
    // SAFETY: the handle belongs to a live `Child` we hold a lock on
    unsafe {
        if on { NtSuspendProcess(handle) } else { NtResumeProcess(handle) };
    }
}

#[cfg(not(windows))]
fn suspend(_child: &Child, _on: bool) {}

#[derive(Default)]
pub struct JobRegistry {
    jobs: Mutex<HashMap<String, Arc<JobCtx>>>,
    counter: AtomicU64,
}

impl JobRegistry {
    pub fn create(&self, app: &AppHandle, kind: &str) -> Arc<JobCtx> {
        let n = self.counter.fetch_add(1, Ordering::SeqCst) + 1;
        let ctx = Arc::new(JobCtx {
            id: format!("{kind}-{n}-{}", std::process::id()),
            app: app.clone(),
            cancelled: AtomicBool::new(false),
            paused: Mutex::new(false),
            resumed: Condvar::new(),
            children: Mutex::new(HashMap::new()),
            next_child: AtomicU64::new(0),
            last_progress: Mutex::new(HashMap::new()),
        });
        self.jobs.lock().unwrap().insert(ctx.id.clone(), ctx.clone());
        ctx
    }

    pub fn get(&self, id: &str) -> Option<Arc<JobCtx>> {
        self.jobs.lock().unwrap().get(id).cloned()
    }

    pub fn remove(&self, id: &str) {
        self.jobs.lock().unwrap().remove(id);
    }

    pub fn any_running(&self) -> bool {
        !self.jobs.lock().unwrap().is_empty()
    }

    pub fn cancel_all(&self) {
        for job in self.jobs.lock().unwrap().values() {
            job.cancel();
        }
    }
}
