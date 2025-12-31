import os
from .base import BaseTab
from ...core.utils import VIDEO_FILTER
from ...core.logic import MkvLogic
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

class OptionsTab(BaseTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = MkvLogic()

    def init_ui(self):
        super().init_ui()
        
        # JSON Selection
        json_layout = QHBoxLayout()
        json_layout.addWidget(QLabel("Options JSON File:"))
        
        self.txt_json_path = QLineEdit()
        self.txt_json_path.setPlaceholderText("Select a JSON file containing mkvmerge options...")
        self.txt_json_path.setReadOnly(True)
        
        self.btn_browse_json = QPushButton("Browse")
        self.btn_browse_json.clicked.connect(self.browse_json)
        
        json_layout.addWidget(self.txt_json_path)
        json_layout.addWidget(self.btn_browse_json)
        
        self.custom_layout.addLayout(json_layout)

    def browse_json(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select JSON Options File", "", "JSON Files (*.json);;All Files (*.*)"
        )
        if file_path:
            self.txt_json_path.setText(file_path)
            self.update_run_button_state()

    def update_run_button_state(self):
        super().update_run_button_state()
        if not self.txt_json_path.text():
            self.btn_run.setEnabled(False)

    def get_file_filter(self):
        return VIDEO_FILTER

    def run_process(self):
        files = self.file_list.get_all_files()
        json_file = self.txt_json_path.text()
        
        if not files or not os.path.exists(json_file):
            return

        jobs = []
        for f in files:
            job = self.logic.get_options_commands(f, json_file)
            jobs.append(job)
            
        self.start_worker(jobs)
