//! Language table shared by the UI, track filters, sidecar detection and translation.
//! Columns: code used in the app (BCP 47 / ISO 639-1), ISO 639-2/B, ISO 639-2/T, English name.

pub type Lang = (&'static str, &'static str, &'static str, &'static str);

pub const LANGS: &[Lang] = &[
    ("ar", "ara", "ara", "Arabic"),
    ("en", "eng", "eng", "English"),
    ("fr", "fre", "fra", "French"),
    ("de", "ger", "deu", "German"),
    ("es", "spa", "spa", "Spanish"),
    ("it", "ita", "ita", "Italian"),
    ("pt", "por", "por", "Portuguese"),
    ("ru", "rus", "rus", "Russian"),
    ("ja", "jpn", "jpn", "Japanese"),
    ("ko", "kor", "kor", "Korean"),
    ("zh", "chi", "zho", "Chinese (Simplified)"),
    ("zh-Hant", "chi", "zho", "Chinese (Traditional)"),
    ("hi", "hin", "hin", "Hindi"),
    ("tr", "tur", "tur", "Turkish"),
    ("fa", "per", "fas", "Persian"),
    ("ur", "urd", "urd", "Urdu"),
    ("he", "heb", "heb", "Hebrew"),
    ("nl", "dut", "nld", "Dutch"),
    ("pl", "pol", "pol", "Polish"),
    ("sv", "swe", "swe", "Swedish"),
    ("no", "nor", "nor", "Norwegian"),
    ("da", "dan", "dan", "Danish"),
    ("fi", "fin", "fin", "Finnish"),
    ("el", "gre", "ell", "Greek"),
    ("cs", "cze", "ces", "Czech"),
    ("sk", "slo", "slk", "Slovak"),
    ("hu", "hun", "hun", "Hungarian"),
    ("ro", "rum", "ron", "Romanian"),
    ("bg", "bul", "bul", "Bulgarian"),
    ("uk", "ukr", "ukr", "Ukrainian"),
    ("sr", "srp", "srp", "Serbian"),
    ("hr", "hrv", "hrv", "Croatian"),
    ("bs", "bos", "bos", "Bosnian"),
    ("sl", "slv", "slv", "Slovenian"),
    ("mk", "mac", "mkd", "Macedonian"),
    ("sq", "alb", "sqi", "Albanian"),
    ("lt", "lit", "lit", "Lithuanian"),
    ("lv", "lav", "lav", "Latvian"),
    ("et", "est", "est", "Estonian"),
    ("is", "ice", "isl", "Icelandic"),
    ("ga", "gle", "gle", "Irish"),
    ("cy", "wel", "cym", "Welsh"),
    ("ca", "cat", "cat", "Catalan"),
    ("eu", "baq", "eus", "Basque"),
    ("gl", "glg", "glg", "Galician"),
    ("id", "ind", "ind", "Indonesian"),
    ("ms", "may", "msa", "Malay"),
    ("th", "tha", "tha", "Thai"),
    ("vi", "vie", "vie", "Vietnamese"),
    ("tl", "tgl", "tgl", "Filipino"),
    ("bn", "ben", "ben", "Bengali"),
    ("ta", "tam", "tam", "Tamil"),
    ("te", "tel", "tel", "Telugu"),
    ("ml", "mal", "mal", "Malayalam"),
    ("kn", "kan", "kan", "Kannada"),
    ("mr", "mar", "mar", "Marathi"),
    ("gu", "guj", "guj", "Gujarati"),
    ("pa", "pan", "pan", "Punjabi"),
    ("ne", "nep", "nep", "Nepali"),
    ("si", "sin", "sin", "Sinhala"),
    ("km", "khm", "khm", "Khmer"),
    ("lo", "lao", "lao", "Lao"),
    ("my", "bur", "mya", "Burmese"),
    ("sw", "swa", "swa", "Swahili"),
    ("am", "amh", "amh", "Amharic"),
    ("so", "som", "som", "Somali"),
    ("ha", "hau", "hau", "Hausa"),
    ("yo", "yor", "yor", "Yoruba"),
    ("zu", "zul", "zul", "Zulu"),
    ("af", "afr", "afr", "Afrikaans"),
    ("ka", "geo", "kat", "Georgian"),
    ("hy", "arm", "hye", "Armenian"),
    ("az", "aze", "aze", "Azerbaijani"),
    ("kk", "kaz", "kaz", "Kazakh"),
    ("uz", "uzb", "uzb", "Uzbek"),
    ("mn", "mon", "mon", "Mongolian"),
    ("ps", "pus", "pus", "Pashto"),
    ("ku", "kur", "kur", "Kurdish"),
    ("la", "lat", "lat", "Latin"),
    ("eo", "epo", "epo", "Esperanto"),
];

/// Finds a language by any of its codes or its English name (case-insensitive).
pub fn find(token: &str) -> Option<&'static Lang> {
    let t = token.trim().to_ascii_lowercase();
    if t.is_empty() {
        return None;
    }
    LANGS.iter().find(|l| {
        l.0.eq_ignore_ascii_case(&t) || l.1 == t || l.2 == t || l.3.eq_ignore_ascii_case(&t)
    })
}

fn base(code: &str) -> &str {
    code.split(['-', '_']).next().unwrap_or("")
}

/// True when a track language (e.g. "eng", "en-US", "ar") matches a wanted code ("en", "ara", ...).
pub fn matches(track_lang: &str, wanted: &str) -> bool {
    let (a, b) = (track_lang.trim(), wanted.trim());
    if a.eq_ignore_ascii_case(b) {
        return true;
    }
    match (find(base(a)), find(base(b))) {
        (Some(x), Some(y)) => x.0 == y.0 || x.1 == y.1,
        _ => base(a).eq_ignore_ascii_case(base(b)) && !base(a).is_empty(),
    }
}

pub fn name(code: &str) -> String {
    find(code)
        .map(|l| l.3.to_string())
        .unwrap_or_else(|| code.to_string())
}

/// Splits "eng, jpn; ara" into tokens.
pub fn tokens(spec: &str) -> Vec<String> {
    spec.split([',', ';', ' '])
        .map(str::trim)
        .filter(|s| !s.is_empty())
        .map(String::from)
        .collect()
}
