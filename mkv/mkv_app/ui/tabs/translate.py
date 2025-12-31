from .base import BaseTab
from ...core.utils import SUBTITLE_FILE_TYPES, SUBTITLE_FILTER
from ...core.logic import MkvLogic
from ...core.settings import AppSettings
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QComboBox

class TranslateTab(BaseTab):
    def __init__(self, parent=None):
        self.settings = AppSettings()
        # Ensure parent init is called after settings
        super().__init__(parent, allowed_extensions=SUBTITLE_FILE_TYPES) 
        self.logic = MkvLogic()

    def init_ui(self):
        super().init_ui()
        
        # Language Selection
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Translate To:"))
        
        self.combo_lang = QComboBox()
        langs = self.settings.get("languageCodes", ["en", "de", "fr", "es", "it"])
        self.combo_lang.addItems(langs)
        
        lang_layout.addWidget(self.combo_lang)
        lang_layout.addStretch()
        
        self.custom_layout.addLayout(lang_layout)

    def get_file_filter(self):
        return SUBTITLE_FILTER

    def run_process(self):
        files = self.file_list.get_all_files()
        lang = self.combo_lang.currentText()
        
        if not files or not lang:
            return

        jobs = []
        for f in files:
            job = self.logic.get_translate_command(f, lang)
            jobs.append(job)
            
        self.start_worker(jobs)
