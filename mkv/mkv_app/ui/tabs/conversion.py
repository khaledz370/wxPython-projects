from .base import BaseTab
from ...core.utils import TO_MKV_FILE_TYPES, DEFAULT_FILE_TYPES, VIDEO_FILTER
from ...core.logic import MkvLogic
from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

class ToMkvTab(BaseTab):
    def __init__(self, parent=None):
        super().__init__(parent, allowed_extensions=TO_MKV_FILE_TYPES) # Original app excluded MKV here
        self.logic = MkvLogic()

    def init_ui(self):
        super().init_ui()
        
        # Custom controls for To MKV
        options_layout = QHBoxLayout()
        
        self.chk_same_folder = QCheckBox("Process in same folder")
        self.chk_same_folder.setChecked(False)
        self.chk_same_folder.setToolTip("Moves original files to a 'mkvmerge_old' subdirectory within the source folder.")
        
        # Output folder override (optional, if they uncheck same folder?)
        # For now, following the 'same folder' logic predominantly as it's safer.
        
        options_layout.addWidget(self.chk_same_folder)
        options_layout.addStretch()
        
        self.custom_layout.addLayout(options_layout)

    def get_file_filter(self):
        return VIDEO_FILTER

    def run_process(self):
        files = self.file_list.get_all_files()
        if not files:
            return

        same_folder = self.chk_same_folder.isChecked()
        jobs = []
        for f in files:
            job = self.logic.get_to_mkv_commands(f, same_folder=same_folder)
            jobs.append(job)
            
        self.start_worker(jobs)


class ToAudioTab(BaseTab):
    def __init__(self, parent=None):
        super().__init__(parent, allowed_extensions=DEFAULT_FILE_TYPES) # MKV allowed for audio extraction
        self.logic = MkvLogic()

    def get_file_filter(self):
        return VIDEO_FILTER

    def run_process(self):
        files = self.file_list.get_all_files()
        if not files:
            return

        jobs = []
        for f in files:
            job = self.logic.get_to_audio_commands(f)
            jobs.append(job)
            
        self.start_worker(jobs)
