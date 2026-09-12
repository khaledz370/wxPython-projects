//! Minimal subtitle model (SRT, WebVTT, ASS/SSA) that keeps timing and styling
//! untouched and only exposes the dialogue text for translation.

use chardetng::EncodingDetector;
use encoding_rs::{Encoding, UTF_8};

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Format {
    Srt,
    Vtt,
    Ass,
}

impl Format {
    pub fn from_ext(ext: &str) -> Option<Self> {
        match ext.to_ascii_lowercase().as_str() {
            "srt" => Some(Self::Srt),
            "vtt" => Some(Self::Vtt),
            "ass" | "ssa" => Some(Self::Ass),
            _ => None,
        }
    }

    /// Matroska codec id → format (text subtitles only).
    pub fn from_codec(codec_id: &str) -> Option<Self> {
        match codec_id.to_ascii_uppercase().as_str() {
            "S_TEXT/UTF8" | "S_TEXT/ASCII" => Some(Self::Srt),
            "S_TEXT/ASS" | "S_TEXT/SSA" => Some(Self::Ass),
            "S_TEXT/WEBVTT" => Some(Self::Vtt),
            _ => None,
        }
    }

    pub fn ext(self) -> &'static str {
        match self {
            Self::Srt => "srt",
            Self::Vtt => "vtt",
            Self::Ass => "ass",
        }
    }
}

struct Cue {
    /// SRT: timing line. VTT: optional id + timing. ASS: "Dialogue: ..." up to the text field.
    head: String,
    text: String,
    /// ASS override tags at the start of the line, e.g. `{\an8}`
    lead: String,
    /// SRT/VTT cue where every line is wrapped in <i>...</i>
    italic: bool,
}

enum Block {
    Raw(String),
    Cue(Cue),
}

pub struct SubDoc {
    format: Format,
    blocks: Vec<Block>,
}

/// Charset of a text file, `None` when it is UTF-8 (or plain ASCII).
pub fn detect_charset(bytes: &[u8]) -> Option<&'static str> {
    if let Some((enc, _)) = Encoding::for_bom(bytes) {
        return (enc != UTF_8).then(|| enc.name());
    }
    if std::str::from_utf8(bytes).is_ok() {
        return None;
    }
    let mut detector = EncodingDetector::new();
    detector.feed(bytes, true);
    Some(detector.guess(None, true).name())
}

pub fn decode(bytes: &[u8]) -> String {
    let encoding = match Encoding::for_bom(bytes) {
        Some((enc, _)) => enc,
        None if std::str::from_utf8(bytes).is_ok() => UTF_8,
        None => {
            let mut detector = EncodingDetector::new();
            detector.feed(bytes, true);
            detector.guess(None, true)
        }
    };
    encoding.decode(bytes).0.into_owned()
}

pub fn parse(text: &str, format: Format) -> SubDoc {
    let text = text.replace("\r\n", "\n").replace('\r', "\n");
    let blocks = match format {
        Format::Srt => parse_srt(&text),
        Format::Vtt => parse_vtt(&text),
        Format::Ass => parse_ass(&text),
    };
    SubDoc { format, blocks }
}

fn split_blocks(text: &str) -> Vec<Vec<&str>> {
    let mut blocks = Vec::new();
    let mut current = Vec::new();
    for line in text.lines() {
        if line.trim().is_empty() {
            if !current.is_empty() {
                blocks.push(std::mem::take(&mut current));
            }
        } else {
            current.push(line);
        }
    }
    if !current.is_empty() {
        blocks.push(current);
    }
    blocks
}

fn make_cue(head: String, lines: &[&str]) -> Cue {
    let italic = !lines.is_empty()
        && lines.iter().all(|l| {
            let t = l.trim();
            t.len() >= 7 && t.starts_with("<i>") && t.ends_with("</i>")
        });
    let text = lines
        .iter()
        .map(|l| {
            let t = l.trim();
            if italic { t[3..t.len() - 4].to_string() } else { t.to_string() }
        })
        .collect::<Vec<_>>()
        .join("\n");
    Cue { head, text, lead: String::new(), italic }
}

fn parse_srt(text: &str) -> Vec<Block> {
    split_blocks(text)
        .into_iter()
        .filter_map(|b| {
            let timing = b.iter().position(|l| l.contains("-->"))?;
            Some(Block::Cue(make_cue(b[timing].trim().to_string(), &b[timing + 1..])))
        })
        .collect()
}

fn parse_vtt(text: &str) -> Vec<Block> {
    split_blocks(text)
        .into_iter()
        .map(|b| match b.iter().position(|l| l.contains("-->")) {
            Some(timing) if !b[0].starts_with("NOTE") => {
                Block::Cue(make_cue(b[..=timing].join("\n"), &b[timing + 1..]))
            }
            _ => Block::Raw(b.join("\n")),
        })
        .collect()
}

fn parse_ass(text: &str) -> Vec<Block> {
    let mut blocks = Vec::new();
    let mut in_events = false;
    let mut fields = 10usize;
    for line in text.lines() {
        let t = line.trim_start();
        if t.starts_with('[') {
            in_events = t.eq_ignore_ascii_case("[events]");
        } else if in_events && t.len() > 7 && t[..7].eq_ignore_ascii_case("format:") {
            fields = t[7..].split(',').count().max(1);
        } else if in_events && t.starts_with("Dialogue:") {
            let body_start = line.len() - t.len() + "Dialogue:".len();
            let body = &line[body_start..];
            let mut commas = 0;
            let split = body.char_indices().find_map(|(i, c)| {
                if c == ',' {
                    commas += 1;
                    if commas == fields - 1 {
                        return Some(i + 1);
                    }
                }
                None
            });
            if let Some(pos) = split {
                let (lead, clean) = split_ass_text(&body[pos..]);
                if !is_drawing(&lead) && !clean.trim().is_empty() {
                    blocks.push(Block::Cue(Cue {
                        head: line[..body_start + pos].to_string(),
                        text: clean,
                        lead,
                        italic: false,
                    }));
                    continue;
                }
            }
        }
        blocks.push(Block::Raw(line.to_string()));
    }
    blocks
}

/// Separates leading `{...}` override blocks, drops inline ones and turns `\N` into newlines.
fn split_ass_text(s: &str) -> (String, String) {
    let mut lead = String::new();
    let mut rest = s;
    while rest.starts_with('{') {
        match rest.find('}') {
            Some(end) => {
                lead.push_str(&rest[..=end]);
                rest = &rest[end + 1..];
            }
            None => break,
        }
    }
    let mut clean = String::new();
    let mut in_tag = false;
    for c in rest.chars() {
        match c {
            '{' => in_tag = true,
            '}' if in_tag => in_tag = false,
            _ if !in_tag => clean.push(c),
            _ => {}
        }
    }
    let clean = clean.replace("\\N", "\n").replace("\\n", " ").replace("\\h", " ");
    (lead, clean)
}

fn is_drawing(lead: &str) -> bool {
    lead.match_indices("\\p")
        .any(|(i, _)| lead[i + 2..].chars().next().is_some_and(|c| c.is_ascii_digit() && c != '0'))
}

impl SubDoc {
    pub fn texts(&self) -> Vec<String> {
        self.blocks
            .iter()
            .filter_map(|b| match b {
                Block::Cue(c) => Some(c.text.clone()),
                Block::Raw(_) => None,
            })
            .collect()
    }

    pub fn set_texts(&mut self, texts: Vec<String>) {
        let mut it = texts.into_iter();
        for block in &mut self.blocks {
            if let Block::Cue(cue) = block {
                if let Some(t) = it.next() {
                    // blank lines would break SRT/VTT blocks
                    cue.text = t
                        .lines()
                        .map(str::trim)
                        .filter(|l| !l.is_empty())
                        .collect::<Vec<_>>()
                        .join("\n");
                }
            }
        }
    }

    pub fn render(&self) -> String {
        match self.format {
            Format::Srt => {
                let mut out = String::new();
                let cues = self.blocks.iter().filter_map(|b| match b {
                    Block::Cue(c) => Some(c),
                    Block::Raw(_) => None,
                });
                for (n, c) in cues.enumerate() {
                    out += &format!("{}\r\n{}\r\n{}\r\n\r\n", n + 1, c.head, cue_text(c).replace('\n', "\r\n"));
                }
                out
            }
            Format::Vtt => {
                let parts: Vec<String> = self
                    .blocks
                    .iter()
                    .map(|b| match b {
                        Block::Raw(s) => s.clone(),
                        Block::Cue(c) => format!("{}\n{}", c.head, cue_text(c)),
                    })
                    .collect();
                parts.join("\n\n") + "\n"
            }
            Format::Ass => {
                let lines: Vec<String> = self
                    .blocks
                    .iter()
                    .map(|b| match b {
                        Block::Raw(s) => s.clone(),
                        Block::Cue(c) => format!("{}{}{}", c.head, c.lead, c.text.replace('\n', "\\N")),
                    })
                    .collect();
                lines.join("\r\n") + "\r\n"
            }
        }
    }
}

fn cue_text(c: &Cue) -> String {
    if c.italic {
        c.text.lines().map(|l| format!("<i>{l}</i>")).collect::<Vec<_>>().join("\n")
    } else {
        c.text.clone()
    }
}

/// UTF-8 with BOM, which every player and mkvmerge recognise.
pub fn to_bytes(text: &str) -> Vec<u8> {
    let mut out = vec![0xEF, 0xBB, 0xBF];
    out.extend_from_slice(text.as_bytes());
    out
}
