//! Subtitle translation with three engines:
//! * Google Translate (free web endpoint, no key)
//! * Google Cloud Translation v2 (API key)
//! * any OpenAI-compatible chat API: Ollama, LM Studio, llama.cpp, vLLM, OpenAI, OpenRouter, ...

use crate::config::{Settings, TranslateSettings};
use crate::files::{self, TempFile};
use crate::jobs::{parse_opts, run_files, FileResult, JobCtx, Outcome, Summary, CANCELLED};
use crate::langs;
use crate::mkv::{self, Tools};
use crate::subtitles::{self, Format};
use reqwest::blocking::Client;
use reqwest::StatusCode;
use serde::Deserialize;
use serde_json::{json, Value};
use std::ffi::OsString;
use std::fs;
use std::path::{Path, PathBuf};
use std::thread;
use std::time::Duration;

pub enum TrError {
    /// The engine returned a different number of lines: retry with smaller batches.
    Mismatch,
    Retry(String),
    Fatal(String),
}

pub trait Translator: Send + Sync {
    /// (max lines per request, max characters per request)
    fn limits(&self) -> (usize, usize);
    fn translate(&self, texts: &[String], src: &str, tgt: &str) -> Result<Vec<String>, TrError>;
}

fn client(timeout_secs: u64) -> Result<Client, String> {
    Client::builder()
        .timeout(Duration::from_secs(timeout_secs.max(10)))
        .user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) MKVBatch/2.0")
        .build()
        .map_err(|e| e.to_string())
}

pub fn build(t: &TranslateSettings) -> Result<Box<dyn Translator>, String> {
    match t.provider.as_str() {
        "google" => Ok(Box::new(GoogleFree { http: client(30)? })),
        "google_cloud" => {
            if t.google_api_key.trim().is_empty() {
                return Err("Google Cloud needs an API key (Translate → Engine)".into());
            }
            Ok(Box::new(GoogleCloud { http: client(60)?, key: t.google_api_key.trim().into() }))
        }
        "openai" => {
            if t.openai_base_url.trim().is_empty() {
                return Err("Enter the server URL of the AI engine".into());
            }
            if t.openai_model.trim().is_empty() {
                return Err("Choose a model for the AI engine".into());
            }
            Ok(Box::new(OpenAi {
                http: client(t.timeout_secs)?,
                base: t.openai_base_url.trim().trim_end_matches('/').into(),
                key: t.openai_api_key.trim().into(),
                model: t.openai_model.trim().into(),
                temperature: t.temperature,
                batch: t.batch_size.clamp(1, 200),
                hint: t.context_hint.trim().into(),
            }))
        }
        other => Err(format!("Unknown translation engine '{other}'")),
    }
}

fn short(body: &str) -> String {
    // error pages are often HTML: keep only the text
    let mut text = String::new();
    let mut in_tag = false;
    for c in body.chars() {
        match c {
            '<' => in_tag = true,
            '>' if in_tag => {
                in_tag = false;
                text.push(' ');
            }
            _ if !in_tag => text.push(c),
            _ => {}
        }
    }
    let text = text.split_whitespace().collect::<Vec<_>>().join(" ");
    let cut: String = text.chars().take(240).collect();
    if cut.len() < text.len() { format!("{cut}…") } else { cut }
}

fn http_error(status: StatusCode, body: &str) -> TrError {
    if status.as_u16() == 429 && body.contains("automated queries") {
        return TrError::Fatal(
            "Google is refusing requests from this network for now (it thinks they are automated). \
             Try again later, or switch the engine to Google Cloud or an AI model."
                .into(),
        );
    }
    let msg = format!("HTTP {}: {}", status.as_u16(), short(body));
    match status.as_u16() {
        401 | 403 => TrError::Fatal(format!("{msg} (check the API key)")),
        404 => TrError::Fatal(format!("{msg} (check the URL / model name)")),
        429 | 500..=599 => TrError::Retry(msg),
        _ => TrError::Fatal(msg),
    }
}

fn send(req: reqwest::blocking::RequestBuilder, what: &str) -> Result<Value, TrError> {
    let resp = req.send().map_err(|e| {
        if e.is_connect() {
            TrError::Fatal(format!("Cannot reach {what}. Is the server running and the URL right?"))
        } else {
            TrError::Retry(e.to_string())
        }
    })?;
    let status = resp.status();
    let body = resp.text().map_err(|e| TrError::Retry(e.to_string()))?;
    if !status.is_success() {
        return Err(http_error(status, &body));
    }
    serde_json::from_str(&body).map_err(|_| TrError::Retry(format!("unexpected reply from {what}: {}", short(&body))))
}

fn google_lang(code: &str) -> String {
    match code {
        "" | "auto" => "auto",
        "zh" => "zh-CN",
        "zh-Hant" => "zh-TW",
        c => c,
    }
    .to_string()
}

/// Splits a long single line into two balanced lines (subtitle style).
fn rewrap(text: &str, lines: usize) -> String {
    if lines < 2 || text.chars().count() <= 42 {
        return text.to_string();
    }
    let mid = text.len() / 2;
    let best = text
        .match_indices(' ')
        .map(|(i, _)| i)
        .min_by_key(|&i| (i as isize - mid as isize).abs());
    match best {
        Some(i) => format!("{}\n{}", text[..i].trim(), text[i + 1..].trim()),
        None => text.to_string(),
    }
}

// --- Google (free web endpoint) --------------------------------------------

struct GoogleFree {
    http: Client,
}

impl Translator for GoogleFree {
    fn limits(&self) -> (usize, usize) {
        (60, 4500)
    }

    fn translate(&self, texts: &[String], src: &str, tgt: &str) -> Result<Vec<String>, TrError> {
        // Every cue becomes one line (sentence context kept); dialogue lines ("- ...") stay separate.
        let mut units = Vec::new();
        let mut shapes = Vec::new();
        for text in texts {
            let lines: Vec<&str> = text.lines().map(str::trim).filter(|l| !l.is_empty()).collect();
            let dialog = lines.len() > 1 && lines.iter().all(|l| l.starts_with('-'));
            if dialog {
                units.extend(lines.iter().map(|l| l.to_string()));
                shapes.push((lines.len(), lines.len(), true));
            } else {
                units.push(lines.join(" "));
                shapes.push((1, lines.len().max(1), false));
            }
        }
        let query = units.join("\n");
        let (sl, tl) = (google_lang(src), google_lang(tgt));
        let req = self
            .http
            .post("https://translate.googleapis.com/translate_a/single")
            .query(&[("client", "gtx"), ("dt", "t"), ("sl", sl.as_str()), ("tl", tl.as_str())])
            .form(&[("q", query.as_str())]);
        let v = send(req, "Google Translate")?;
        let mut joined = String::new();
        for part in v[0].as_array().into_iter().flatten() {
            if let Some(s) = part[0].as_str() {
                joined.push_str(s);
            }
        }
        let out_units: Vec<String> = joined.split('\n').map(|s| s.trim().to_string()).collect();
        if out_units.len() != units.len() {
            return Err(TrError::Mismatch);
        }
        let mut it = out_units.into_iter();
        Ok(shapes
            .into_iter()
            .map(|(count, lines, dialog)| {
                if dialog {
                    it.by_ref().take(count).collect::<Vec<_>>().join("\n")
                } else {
                    rewrap(&it.next().unwrap_or_default(), lines)
                }
            })
            .collect())
    }
}

// --- Google Cloud Translation v2 --------------------------------------------

struct GoogleCloud {
    http: Client,
    key: String,
}

impl Translator for GoogleCloud {
    fn limits(&self) -> (usize, usize) {
        (100, 9000)
    }

    fn translate(&self, texts: &[String], src: &str, tgt: &str) -> Result<Vec<String>, TrError> {
        let mut body = json!({ "q": texts, "target": google_lang(tgt), "format": "text" });
        if !src.is_empty() && src != "auto" {
            body["source"] = json!(google_lang(src));
        }
        let req = self
            .http
            .post("https://translation.googleapis.com/language/translate/v2")
            .query(&[("key", self.key.as_str())])
            .json(&body);
        let v = send(req, "Google Cloud Translation")?;
        let out: Vec<String> = v["data"]["translations"]
            .as_array()
            .into_iter()
            .flatten()
            .map(|t| t["translatedText"].as_str().unwrap_or("").to_string())
            .collect();
        if out.len() != texts.len() {
            return Err(TrError::Mismatch);
        }
        Ok(out)
    }
}

// --- OpenAI-compatible chat API ---------------------------------------------

struct OpenAi {
    http: Client,
    base: String,
    key: String,
    model: String,
    temperature: f32,
    batch: usize,
    hint: String,
}

impl Translator for OpenAi {
    fn limits(&self) -> (usize, usize) {
        (self.batch, 6000)
    }

    fn translate(&self, texts: &[String], src: &str, tgt: &str) -> Result<Vec<String>, TrError> {
        let src_name = if src.is_empty() || src == "auto" {
            "the source language (detect it)".to_string()
        } else {
            langs::name(src)
        };
        let mut system = format!(
            "You are a professional subtitle translator. Translate every item of the JSON array \"lines\" \
             from {src_name} into {tgt_name}.\n\
             Rules:\n\
             - Reply with ONLY a JSON object of the form {{\"t\": [\"...\"]}} containing exactly {n} strings, in the same order.\n\
             - Never merge, split, skip or reorder items.\n\
             - Keep line breaks (\\n) and markup such as <i> and </i>.\n\
             - Use natural, concise subtitle language. Keep names as they are.\n\
             - No notes, explanations or transliterations.",
            tgt_name = langs::name(tgt),
            n = texts.len()
        );
        if !self.hint.is_empty() {
            system += &format!("\nContext from the user: {}", self.hint);
        }
        let mut body = json!({
            "model": self.model,
            "stream": false,
            "messages": [
                { "role": "system", "content": system },
                { "role": "user", "content": json!({ "lines": texts }).to_string() }
            ]
        });
        if self.temperature >= 0.0 {
            body["temperature"] = json!(self.temperature);
        }
        let mut req = self.http.post(format!("{}/chat/completions", self.base)).json(&body);
        if !self.key.is_empty() {
            req = req.bearer_auth(&self.key);
        }
        let v = send(req, &self.base)?;
        let content = v["choices"][0]["message"]["content"].as_str().unwrap_or("");
        let out = parse_llm_array(content).ok_or(TrError::Mismatch)?;
        if out.len() != texts.len() {
            return Err(TrError::Mismatch);
        }
        Ok(out)
    }
}

/// Pulls the translated array out of a model reply, tolerating reasoning blocks,
/// code fences and chatty text around the JSON.
fn parse_llm_array(content: &str) -> Option<Vec<String>> {
    let mut s = content.to_string();
    while let Some(start) = s.find("<think>") {
        match s[start..].find("</think>") {
            Some(end) => s.replace_range(start..start + end + "</think>".len(), ""),
            None => s.truncate(start),
        }
    }
    let s = s.trim();
    let slice = |open: char, close: char| -> String {
        match (s.find(open), s.rfind(close)) {
            (Some(a), Some(b)) if b > a => s[a..=b].to_string(),
            _ => String::new(),
        }
    };
    [s.to_string(), slice('{', '}'), slice('[', ']')]
        .iter()
        .filter_map(|c| serde_json::from_str::<Value>(c).ok())
        .find_map(|v| pick_array(&v))
}

fn pick_array(v: &Value) -> Option<Vec<String>> {
    let arr = match v {
        Value::Array(a) => a,
        Value::Object(o) => ["t", "translations", "lines"]
            .iter()
            .find_map(|k| o.get(*k).and_then(Value::as_array))
            .or_else(|| o.values().find_map(Value::as_array))?,
        _ => return None,
    };
    arr.iter()
        .map(|x| match x {
            Value::String(s) => Some(s.clone()),
            Value::Object(o) => o.get("text").or(o.get("t")).and_then(Value::as_str).map(String::from),
            Value::Number(n) => Some(n.to_string()),
            _ => None,
        })
        .collect()
}

// --- batching / retries -------------------------------------------------------

pub fn translate_texts(
    tr: &dyn Translator,
    texts: &[String],
    src: &str,
    tgt: &str,
    cancelled: &dyn Fn() -> bool,
    progress: &mut dyn FnMut(usize, usize),
    warn: &mut dyn FnMut(String),
) -> Result<Vec<String>, String> {
    let mut out = texts.to_vec();
    let (max_items, max_chars) = tr.limits();
    let mut batches: Vec<Vec<usize>> = Vec::new();
    let mut current = Vec::new();
    let mut chars = 0;
    for i in (0..texts.len()).filter(|&i| !texts[i].trim().is_empty()) {
        let len = texts[i].chars().count();
        if !current.is_empty() && (current.len() >= max_items || chars + len > max_chars) {
            batches.push(std::mem::take(&mut current));
            chars = 0;
        }
        current.push(i);
        chars += len;
    }
    if !current.is_empty() {
        batches.push(current);
    }

    let total: usize = batches.iter().map(Vec::len).sum();
    let mut done = 0;
    progress(0, total);
    for batch in batches {
        let input: Vec<String> = batch.iter().map(|&i| texts[i].clone()).collect();
        let result = translate_robust(tr, &input, src, tgt, cancelled, warn)?;
        for (k, &i) in batch.iter().enumerate() {
            out[i] = result[k].clone();
        }
        done += batch.len();
        progress(done, total);
    }
    Ok(out)
}

fn translate_robust(
    tr: &dyn Translator,
    input: &[String],
    src: &str,
    tgt: &str,
    cancelled: &dyn Fn() -> bool,
    warn: &mut dyn FnMut(String),
) -> Result<Vec<String>, String> {
    let mut attempt = 0u64;
    loop {
        if cancelled() {
            return Err(CANCELLED.into());
        }
        match tr.translate(input, src, tgt) {
            Ok(v) => return Ok(v),
            Err(TrError::Fatal(e)) => return Err(e),
            Err(TrError::Mismatch) if input.len() > 1 => {
                let mid = input.len() / 2;
                let mut first = translate_robust(tr, &input[..mid], src, tgt, cancelled, warn)?;
                first.extend(translate_robust(tr, &input[mid..], src, tgt, cancelled, warn)?);
                return Ok(first);
            }
            Err(TrError::Mismatch) => {
                attempt += 1;
                if attempt >= 2 {
                    warn(format!("could not translate \"{}\", kept the original line", short(&input[0])));
                    return Ok(input.to_vec());
                }
            }
            Err(TrError::Retry(e)) => {
                attempt += 1;
                if attempt > 4 {
                    return Err(e);
                }
                warn(format!("{e}, retrying ({attempt}/4)"));
                for _ in 0..attempt * 20 {
                    if cancelled() {
                        return Err(CANCELLED.into());
                    }
                    thread::sleep(Duration::from_millis(100));
                }
            }
        }
    }
}

// --- UI helpers ---------------------------------------------------------------

pub fn list_models(t: &TranslateSettings) -> Result<Vec<String>, String> {
    let http = client(20)?;
    let base = t.openai_base_url.trim().trim_end_matches('/');
    let mut req = http.get(format!("{base}/models"));
    if !t.openai_api_key.trim().is_empty() {
        req = req.bearer_auth(t.openai_api_key.trim());
    }
    let v = send(req, base).map_err(|e| match e {
        TrError::Fatal(m) | TrError::Retry(m) => m,
        TrError::Mismatch => "unexpected reply".into(),
    })?;
    let mut models: Vec<String> = v["data"]
        .as_array()
        .or(v["models"].as_array())
        .into_iter()
        .flatten()
        .filter_map(|m| m["id"].as_str().or(m["name"].as_str()).map(String::from))
        .collect();
    models.sort();
    Ok(models)
}

pub fn test(t: &TranslateSettings, target: &str) -> Result<String, String> {
    let tr = build(t)?;
    let sample = vec!["Hello! How are you today?".to_string()];
    let out = translate_robust(tr.as_ref(), &sample, "en", target, &|| false, &mut |_| {})?;
    Ok(out.join(" "))
}

// --- the job --------------------------------------------------------------------

#[derive(Deserialize)]
#[serde(default, rename_all = "camelCase")]
struct TranslateOpts {
    source: String,
    target: String,
    track_lang: String,
    mux_back: bool,
    set_default: bool,
}

impl Default for TranslateOpts {
    fn default() -> Self {
        Self {
            source: "auto".into(),
            target: String::new(),
            track_lang: String::new(),
            mux_back: false,
            set_default: false,
        }
    }
}

pub fn job(ctx: &JobCtx, s: &Settings, list: &[PathBuf], opts: Value) -> Result<Summary, String> {
    let o: TranslateOpts = parse_opts(opts)?;
    if o.target.trim().is_empty() {
        return Err("Choose a target language".into());
    }
    let tr = build(&s.translate)?;
    let tools = if list.iter().any(|f| mkv::is_matroska(f)) { Some(mkv::tools(s)?) } else { None };
    let scratch = ctx.temp_dir()?;
    Ok(run_files(ctx, list, 1, |i, f| {
        translate_one(ctx, s, tr.as_ref(), tools.as_ref(), &o, &scratch, i, f)
    }))
}

/// `Movie.en` → `Movie` so the output becomes `Movie.ar.srt`, not `Movie.en.ar.srt`.
fn stem_without_lang(file: &Path) -> String {
    let stem = files::stem_of(file);
    match stem.rsplit_once('.') {
        Some((base, last)) if !base.is_empty() && langs::find(last).is_some() => base.to_string(),
        _ => stem,
    }
}

#[allow(clippy::too_many_arguments)]
fn translate_one(
    ctx: &JobCtx,
    s: &Settings,
    tr: &dyn Translator,
    tools: Option<&Tools>,
    o: &TranslateOpts,
    scratch: &Path,
    index: usize,
    file: &Path,
) -> FileResult {
    let name = files::name_of(file);
    let is_mkv = mkv::is_matroska(file);
    let mut src = if o.source.trim().is_empty() { "auto".to_string() } else { o.source.clone() };

    // 1. get the subtitle text
    let mut mkv_context = None;
    let (sub_path, format) = if is_mkv {
        let t = tools.ok_or("MKVToolNix is required for MKV files")?;
        let info = mkv::identify(&t.mkvmerge, file)?;
        let track = info
            .tracks
            .iter()
            .filter(|t| t.kind == "subtitles" && Format::from_codec(&t.codec_id).is_some())
            .find(|t| o.track_lang.trim().is_empty() || langs::matches(&t.language, &o.track_lang))
            .cloned();
        let Some(track) = track else {
            return Ok(Outcome::Skipped(
                "no matching text subtitle track (PGS / VobSub images can't be translated)".into(),
            ));
        };
        let format = Format::from_codec(&track.codec_id).unwrap();
        let extracted = scratch.join(format!("{index}-track{}.{}", track.id, format.ext()));
        let args: Vec<OsString> = vec![
            "--ui-language".into(),
            "en".into(),
            "--gui-mode".into(),
            file.into(),
            "tracks".into(),
            format!("{}:{}", track.id, extracted.display()).into(),
        ];
        mkv::run_tool(ctx, index, &t.mkvextract, &args, (0.0, 5.0))?;
        if src == "auto" && track.language != "und" {
            src = track.language.clone();
        }
        mkv_context = Some((t, info));
        (extracted, format)
    } else {
        let format = Format::from_ext(&files::ext_of(file))
            .ok_or("unsupported subtitle format (SRT, VTT, ASS and SSA are supported)")?;
        (file.to_path_buf(), format)
    };

    // 2. translate
    let bytes = fs::read(&sub_path).map_err(|e| format!("Can't read subtitles: {e}"))?;
    let mut doc = subtitles::parse(&subtitles::decode(&bytes), format);
    let texts = doc.texts();
    if texts.is_empty() {
        return Ok(Outcome::Skipped("no subtitle lines found".into()));
    }
    let (from, span) = if is_mkv { (5.0, 85.0) } else { (0.0, 98.0) };
    let mut warnings = 0;
    let translated = translate_texts(
        tr,
        &texts,
        &src,
        &o.target,
        &|| ctx.is_cancelled(),
        &mut |done, total| ctx.progress(index, from + span * done as f32 / total.max(1) as f32),
        &mut |w| {
            warnings += 1;
            ctx.log("warn", &format!("{name}: {w}"));
        },
    )?;
    doc.set_texts(translated);
    let data = subtitles::to_bytes(&doc.render());
    let target_ext = if is_mkv { format.ext().to_string() } else { files::ext_of(file) };
    let lang_name = langs::name(&o.target);

    // 3a. put it back into the MKV as a new track
    if let (true, Some((t, info))) = (o.mux_back, mkv_context) {
        let sub_file = scratch.join(format!("{index}-translated.{target_ext}"));
        fs::write(&sub_file, &data).map_err(|e| format!("Can't write subtitles: {e}"))?;
        let out = file.to_path_buf();
        let tmp = TempFile::new(files::temp_sibling(&out));
        let mut a: Vec<OsString> = vec!["--ui-language".into(), "en".into(), "--gui-mode".into()];
        a.extend(["-o".into(), tmp.path().into()]);
        if o.set_default {
            for track in info.of_kind("subtitles") {
                a.extend(["--default-track-flag".into(), format!("{}:no", track.id).into()]);
            }
        }
        a.push(file.into());
        a.extend([
            "--language".into(),
            format!("0:{}", o.target).into(),
            "--track-name".into(),
            format!("0:{lang_name}").into(),
            "--default-track-flag".into(),
            (if o.set_default { "0:yes" } else { "0:no" }).into(),
            "--sub-charset".into(),
            "0:UTF-8".into(),
            sub_file.into(),
        ]);
        files::check_space(&out, files::size_of(file))?;
        mkv::run_tool(ctx, index, &t.mkvmerge, &a, (90.0, 100.0))?;
        let fin = files::finalize(s, file, tmp.path(), &out)?;
        let msg = format!("{} lines → {lang_name} track in {}", texts.len(), files::name_of(&fin.path));
        return Ok(if fin.warning || warnings > 0 { Outcome::Warn(msg) } else { Outcome::Done(msg) });
    }

    // 3b. write a sidecar file
    let dir = file.parent().unwrap_or(Path::new("."));
    let out = files::unique_path(&dir.join(format!("{}.{}.{target_ext}", stem_without_lang(file), o.target)));
    files::write_atomic(&out, &data)?;
    let msg = format!("{} lines → {}", texts.len(), files::name_of(&out));
    Ok(if warnings > 0 { Outcome::Warn(msg) } else { Outcome::Done(msg) })
}
