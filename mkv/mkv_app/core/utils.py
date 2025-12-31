import os

# File Type Constants
DEFAULT_FILE_TYPES = [
    ".mkv", ".ts", ".mp4", ".avi", ".webm", ".flv", ".ogg", ".mov", ".mpeg-2"
]

TO_MKV_FILE_TYPES = [
    ".ts", ".mp4", ".avi", ".webm", ".flv", ".ogg", ".mov", ".mpeg-2"
]

SUBTITLE_FILE_TYPES = [
    ".srt", ".sub", ".sbv", ".ass", ".ssa", ".usf", ".idx", ".aqt", 
    ".jss", ".psb", ".rt", ".smi", ".stl", ".vtt", ".xml", ".txt"
]

# Filters for QFileDialog
VIDEO_FILTER = "Videos (*.mkv *.ts *.mp4 *.avi *.webm *.flv *.ogg *.mov *.mpeg-2);;All files (*.*)"
SUBTITLE_FILTER = "Subtitles (*.srt *.sub *.sbv *.ass *.ssa *.usf *.idx *.aqt *.jss *.psb *.rt *.smi *.stl *.vtt *.xml *.txt);;All files (*.*)"

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
