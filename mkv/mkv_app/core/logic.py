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
        
        mkvmerge_dir = output_dir if output_dir else source_dir
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
