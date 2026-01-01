import os
import shutil

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

# Image File Types for conversion
IMAGE_FILE_TYPES = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", 
    ".webp", ".ico", ".svg", ".heic", ".heif", ".raw", ".psd"
]

# Supported output image formats for conversion
IMAGE_OUTPUT_FORMATS = [
    ("ICO", ".ico"),
    ("WebP", ".webp"),
    ("PNG", ".png"),
    ("JPEG", ".jpg"),
    ("GIF", ".gif"),
    ("BMP", ".bmp"),
    ("TIFF", ".tiff"),
]

# Filters for QFileDialog
VIDEO_FILTER = "Videos (*.mkv *.ts *.mp4 *.avi *.webm *.flv *.ogg *.mov *.mpeg-2);;All files (*.*)"
SUBTITLE_FILTER = "Subtitles (*.srt *.sub *.sbv *.ass *.ssa *.usf *.idx *.aqt *.jss *.psb *.rt *.smi *.stl *.vtt *.xml *.txt);;All files (*.*)"
IMAGE_FILTER = "Images (*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp *.ico *.svg *.heic *.heif *.raw *.psd);;All files (*.*)"

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_ffmpeg_available():
    """Check if ffmpeg is available in the system PATH."""
    ffmpeg_path = shutil.which("ffmpeg")
    return ffmpeg_path is not None

def get_ffmpeg_path():
    """Get the path to ffmpeg executable if available."""
    return shutil.which("ffmpeg")
