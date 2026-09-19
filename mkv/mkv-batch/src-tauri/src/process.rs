//! Spawning external tools (mkvmerge, ffmpeg, ...) without console windows,
//! streaming their output line by line and killing them on cancel.

use crate::jobs::{JobCtx, CANCELLED};
use std::io::Read;
use std::path::Path;
use std::process::{Command, Stdio};
use std::sync::mpsc::{self, RecvTimeoutError, Sender};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

#[cfg(windows)]
use std::os::windows::process::CommandExt;

#[cfg(windows)]
const CREATE_NO_WINDOW: u32 = 0x0800_0000;

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum Stream {
    Out,
    Err,
}

/// A `Command` that never flashes a console window.
pub fn command(program: &Path) -> Command {
    let mut cmd = Command::new(program);
    #[cfg(windows)]
    cmd.creation_flags(CREATE_NO_WINDOW);
    cmd.stdin(Stdio::null());
    cmd
}

/// Human readable command line, used for the activity log.
pub fn describe(cmd: &Command) -> String {
    let quote = |s: String| {
        if s.is_empty() || s.contains(' ') {
            format!("\"{s}\"")
        } else {
            s
        }
    };
    let program = Path::new(cmd.get_program())
        .file_name()
        .map(|n| n.to_string_lossy().into_owned())
        .unwrap_or_default();
    let args: Vec<String> = cmd
        .get_args()
        .map(|a| quote(a.to_string_lossy().into_owned()))
        .collect();
    format!("{program} {}", args.join(" "))
}

/// Runs `cmd`, calling `on_line` for every stdout/stderr line (split on `\n` and `\r`,
/// so carriage-return progress output is seen too). Returns the exit code.
/// Returns `Err(CANCELLED)` when the job was cancelled; the process is killed.
pub fn run(
    ctx: &JobCtx,
    mut cmd: Command,
    mut on_line: impl FnMut(Stream, &str),
) -> Result<i32, String> {
    ctx.wait_if_paused();
    if ctx.is_cancelled() {
        return Err(CANCELLED.into());
    }
    ctx.log("cmd", &describe(&cmd));
    cmd.stdout(Stdio::piped()).stderr(Stdio::piped());

    let program = Path::new(cmd.get_program())
        .file_name()
        .map(|n| n.to_string_lossy().into_owned())
        .unwrap_or_default();
    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Could not start {program}: {e}"))?;
    let stdout = child.stdout.take().expect("piped stdout");
    let stderr = child.stderr.take().expect("piped stderr");

    let (tx, rx) = mpsc::channel::<(Stream, String)>();
    let tx_err = tx.clone();
    let out_thread = thread::spawn(move || pump(stdout, Stream::Out, tx));
    let err_thread = thread::spawn(move || pump(stderr, Stream::Err, tx_err));

    let child = Arc::new(Mutex::new(child));
    let key = ctx.register_child(child.clone());

    loop {
        match rx.recv_timeout(Duration::from_millis(150)) {
            Ok((stream, line)) => on_line(stream, &line),
            Err(RecvTimeoutError::Timeout) => {
                if ctx.is_cancelled() {
                    let _ = child.lock().unwrap().kill();
                }
            }
            Err(RecvTimeoutError::Disconnected) => break,
        }
    }
    let _ = out_thread.join();
    let _ = err_thread.join();
    let status = child.lock().unwrap().wait();
    ctx.unregister_child(key);

    if ctx.is_cancelled() {
        return Err(CANCELLED.into());
    }
    status
        .map(|s| s.code().unwrap_or(-1))
        .map_err(|e| format!("{program}: {e}"))
}

fn pump(mut reader: impl Read, stream: Stream, tx: Sender<(Stream, String)>) {
    let mut buf = [0u8; 8192];
    let mut line = Vec::new();
    loop {
        let n = match reader.read(&mut buf) {
            Ok(0) | Err(_) => break,
            Ok(n) => n,
        };
        for &b in &buf[..n] {
            if b == b'\n' || b == b'\r' {
                if !line.is_empty() {
                    let text = String::from_utf8_lossy(&line).into_owned();
                    if tx.send((stream, text)).is_err() {
                        return;
                    }
                    line.clear();
                }
            } else {
                line.push(b);
            }
        }
    }
    if !line.is_empty() {
        let _ = tx.send((stream, String::from_utf8_lossy(&line).into_owned()));
    }
}
