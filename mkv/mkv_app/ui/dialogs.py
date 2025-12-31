from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QPushButton, QDialogButtonBox, QFileDialog, QHBoxLayout, QMessageBox
)
from ..core.settings import AppSettings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(450, 150)
        self.settings = AppSettings()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # MKVToolNix Path
        self.txt_mkv_path = QLineEdit(self.settings.get("mkvtoolnix"))
        btn_browse = QPushButton("...")
        btn_browse.setFixedWidth(30)
        btn_browse.clicked.connect(self.browse_mkv_path)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.txt_mkv_path)
        path_layout.addWidget(btn_browse)
        
        form.addRow("MKVToolNix Path:", path_layout)
        
        # Languages (Comma separated)
        self.txt_langs = QLineEdit(", ".join(self.settings.get("languageCodes")))
        form.addRow("Languages (csv):", self.txt_langs)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_settings)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)

    def browse_mkv_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select MKVToolNix Directory")
        if path:
            self.txt_mkv_path.setText(path)

    def save_settings(self):
        mkv_path = self.txt_mkv_path.text().strip()
        langs_str = self.txt_langs.text().strip()
        
        langs = [l.strip() for l in langs_str.split(",") if l.strip()]
        
        self.settings.set("mkvtoolnix", mkv_path)
        self.settings.set("languageCodes", langs)
        
        QMessageBox.information(self, "Settings Saved", "Settings have been saved. Restart may be required for some changes.")
        self.accept()
