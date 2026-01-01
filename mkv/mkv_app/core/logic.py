import os
import shutil
import json
from .settings import AppSettings
from .utils import ensure_dir_exists

class MkvLogic:
    def __init__(self):
        self.settings = AppSettings()

    def get_to_mkv_commands(self, file_path, output_dir=None, same_folder=False):
        """
        Generates commands for 'To MKV' conversion.
        Returns a list of steps. Each step is a dict with 'type', 'command', etc.
        """
        f_name = os.path.basename(file_path)
        f_name_no_ext = os.path.splitext(f_name)[0]
        source_dir = os.path.dirname(file_path)
        
        mkvmerge_dir = output_dir if output_dir else os.path.splitdrive(file_path)[0] + os.sep  # Root of drive
        if same_folder:
            mkvmerge_dir = source_dir

        # Logic from original:
        # 1. Move file to mkvmerge_old folder
        # 2. Run mkvmerge to create new mkv at dest
        
        old_dir = os.path.join(mkvmerge_dir, "mkvmerge_old")
        moved_file_path = os.path.join(old_dir, f_name)
        output_file = os.path.join(source_dir, f"{f_name_no_ext}.mkv")
        
        # We return a comprehensive "job" object that the worker can execute
        return {
            "type": "to_mkv",
            "source_file": file_path,
            "moved_file_path": moved_file_path,
            "output_file": output_file,
            "mkvmerge_path": self.settings.mkvmerge_path
        }

    def get_to_audio_commands(self, file_path):
        f_name = os.path.basename(file_path)
        f_name_no_ext = os.path.splitext(f_name)[0]
        source_dir = os.path.dirname(file_path)
        
        output_dir = os.path.join(source_dir, "audio")
        output_file = os.path.join(output_dir, f"{f_name_no_ext}.mka")
        
        cmd = f'"{self.settings.mkvmerge_path}" --output "{output_file}" --no-video --language 1:und "{file_path}"'
        
        return {
            "type": "command",
            "command": cmd,
            "description": f"Extracting audio from {f_name}",
            "ensure_dir": output_dir
        }

    def get_crop_commands(self, file_path, top, left, right, bottom):
        """
        Returns a list of commands for cropping.
        1. Move to 'old'
        2. Convert to mkv (if not already mkv)
        3. Remove existing crop
        4. Set new crop
        """
        f_name = os.path.basename(file_path)
        f_name_no_ext = os.path.splitext(f_name)[0]
        ext = os.path.splitext(f_name)[1].lower()
        source_dir = os.path.dirname(file_path)
        
        steps = []
        
        # If not MKV, convert first
        input_file_for_crop = file_path
        if ext != ".mkv":
            old_dir = os.path.join(source_dir, "old")
            moved_file_path = os.path.join(old_dir, f_name)
            output_converted = os.path.join(source_dir, f"{f_name_no_ext}.mkv")
            
            steps.append({
                "type": "move_and_convert",
                "source_file": file_path,
                "moved_file_path": moved_file_path,
                "output_file": output_converted,
                "mkvmerge_path": self.settings.mkvmerge_path
            })
            input_file_for_crop = output_converted
        else:
            # Even if MKV, original logic implies editing in place, handled by mkvpropedit
            pass

        # Remove existing crop
        remove_cmd = f'"{self.settings.mkvpropedit_path}" "{input_file_for_crop}" --edit track:v1 --delete pixel-crop-top --delete pixel-crop-left --delete pixel-crop-right --delete pixel-crop-bottom'
        steps.append({
            "type": "command",
            "command": remove_cmd,
            "description": "Removing existing crop"
        })
        
        # Set new crop
        set_cmd = f'"{self.settings.mkvpropedit_path}" "{input_file_for_crop}" --edit track:v1 --set pixel-crop-top={top} --set pixel-crop-left={left} --set pixel-crop-right={right} --set pixel-crop-bottom={bottom}'
        steps.append({
            "type": "command",
            "command": set_cmd,
            "description": "Setting new crop properties"
        })
        
        return steps

    def get_options_commands(self, file_path, json_file):
        f_name = os.path.basename(file_path)
        f_name_no_ext = os.path.splitext(f_name)[0]
        source_dir = os.path.dirname(file_path)
        
        mkvmerge_old_dir = os.path.join(source_dir, "mkvmerge_old")
        moved_file_path = os.path.join(mkvmerge_old_dir, f_name)
        output_file = os.path.join(source_dir, f"{f_name_no_ext}.mkv")
        
        cmd = f'"{self.settings.mkvmerge_path}" @"{json_file}" -o "{output_file}" "{moved_file_path}"'
        
        return {
            "type": "to_options",
            "source_file": file_path,
            "moved_file_path": moved_file_path,
            "output_file": output_file,
            "command_template": f'"{self.settings.mkvmerge_path}" @"{{json_file}}" -o "{{output_file}}" "{{input_file}}"',
            "json_file": json_file
        }

    def get_translate_command(self, file_path, lang_code, attempt=0):
        f_name = os.path.basename(file_path)
        f_name_no_ext = os.path.splitext(f_name)[0]
        source_dir = os.path.dirname(file_path)
        
        suffix = f"_{attempt}" if attempt > 0 else ""
        output_file = os.path.join(source_dir, f"{f_name_no_ext}.{lang_code}{suffix}.srt")
        
        if os.path.exists(output_file):
            return self.get_translate_command(file_path, lang_code, attempt + 1)
            
        cmd = f'translatesubs "{file_path}" "{output_file}" --tolang {lang_code}'
        
        return {
            "type": "command",
            "command": cmd,
            "description": f"Translating {f_name} to {lang_code}"
        }

    def get_image_conversion_command(self, file_path, output_format, same_folder=False):
        """
        Generates command for image format conversion using ffmpeg.
        
        Args:
            file_path: Path to the source image file
            output_format: Target format extension (e.g., '.jpg', '.png')
            same_folder: If True, output to same folder as source. If False, output to 'converted_images' subfolder.
        
        Returns:
            A job dict for the worker thread
        """
        from .utils import get_ffmpeg_path
        
        f_name = os.path.basename(file_path)
        f_name_no_ext = os.path.splitext(f_name)[0]
        source_dir = os.path.dirname(file_path)
        
        # Determine output directory
        if same_folder:
            output_dir = source_dir
        else:
            # Output to 'converted_images' folder in drive root (e.g., D:\converted_images\)
            drive_root = os.path.splitdrive(file_path)[0]
            if drive_root: # If a drive letter exists (Windows)
                output_dir = os.path.join(drive_root + os.sep, "converted_images")
            else: # Unix-like or relative path, use source_dir as base
                output_dir = os.path.join(source_dir, "converted_images")
        
        # Create output filename with format suffix and new extension
        # e.g., "image.png" -> "image_jpg.jpg" when converting to JPEG
        format_suffix = output_format.lstrip('.')  # Remove the leading dot (e.g., ".jpg" -> "jpg")
        
        # Check if file exists and add incremental suffix if needed
        base_output = os.path.join(output_dir, f"{f_name_no_ext}_{format_suffix}")
        output_file = f"{base_output}{output_format}"
        
        counter = 1
        while os.path.exists(output_file):
            output_file = f"{base_output}_{counter:02d}{output_format}"
            counter += 1
        
        # Get ffmpeg path
        ffmpeg_path = get_ffmpeg_path()
        if not ffmpeg_path:
            ffmpeg_path = "ffmpeg"  # Fallback to PATH
        
        # Build ffmpeg command with proper flags for image conversion
        # -y: Overwrite output without asking
        # -i: Input file
        # -frames:v 1: Output only 1 frame (for single image)
        
        # Format-specific options
        filter_opts = ""
        quality_opts = ""
        
        if output_format in [".jpg", ".jpeg"]:
            quality_opts = "-q:v 2"  # High quality JPEG (2-31, lower is better)
        elif output_format == ".png":
            quality_opts = ""  # PNG uses lossless compression by default
        elif output_format == ".webp":
            quality_opts = "-quality 90"  # High quality WebP
        elif output_format == ".ico":
            # ICO format has max 256x256 dimension limit
            # Scale down while maintaining aspect ratio if larger
            filter_opts = '-vf "scale=\'min(256,iw)\':\'min(256,ih)\':force_original_aspect_ratio=decrease"'
        elif output_format == ".bmp":
            quality_opts = ""  # BMP is uncompressed
        elif output_format == ".gif":
            quality_opts = ""  # Single frame GIF
        elif output_format == ".tiff":
            quality_opts = ""  # TIFF default compression
        
        # Build the command
        cmd = f'"{ffmpeg_path}" -y -i "{file_path}" -frames:v 1 {filter_opts} {quality_opts} "{output_file}"'
        
        # Clean up any double spaces from empty options
        cmd = ' '.join(cmd.split())
        
        # Build job dict
        job = {
            "type": "command",
            "command": cmd,
            "description": f"Converting {f_name} to {output_format}",
            "source_file": file_path
        }
        
        # Only include ensure_dir if output is to a different directory than source
        if output_dir != source_dir:
            job["ensure_dir"] = output_dir
        
        return job
