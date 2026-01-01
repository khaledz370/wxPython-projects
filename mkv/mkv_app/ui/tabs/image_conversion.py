"""
Image Conversion Tab - Converts images to various formats using ffmpeg.
"""
from .base import BaseTab
from ...core.utils import (
    IMAGE_FILE_TYPES, IMAGE_FILTER, IMAGE_OUTPUT_FORMATS, 
    is_ffmpeg_available
)
from ...core.logic import MkvLogic
from PyQt6.QtWidgets import (
    QCheckBox, QHBoxLayout, QLabel, QComboBox, QMessageBox, QVBoxLayout,
    QFrame
)
from PyQt6.QtCore import Qt


class ImageConversionTab(BaseTab):
    """Tab for converting images to different formats using ffmpeg."""
    
    def __init__(self, parent=None):
        # Check if ffmpeg is available before initializing
        self.ffmpeg_available = is_ffmpeg_available()
        super().__init__(parent, allowed_extensions=IMAGE_FILE_TYPES)
        self.logic = MkvLogic()

    def init_ui(self):
        super().init_ui()
        
        # If ffmpeg is not available, show a warning message
        if not self.ffmpeg_available:
            self._show_ffmpeg_warning()
            return
        
        # Options container frame for better visual grouping
        options_frame = QFrame()
        options_frame.setObjectName("optionsFrame")
        options_layout = QVBoxLayout(options_frame)
        options_layout.setContentsMargins(10, 10, 10, 10)
        
        # Row 1: Output format selection
        format_layout = QHBoxLayout()
        
        lbl_format = QLabel("Output Format:")
        lbl_format.setMinimumWidth(100)
        
        self.cmb_format = QComboBox()
        self.cmb_format.setMinimumWidth(150)
        for name, ext in IMAGE_OUTPUT_FORMATS:
            self.cmb_format.addItem(f"{name} ({ext})", ext)
        self.cmb_format.setCurrentIndex(0)  # Default to first format (JPEG)
        self.cmb_format.setToolTip("Select the output image format")
        
        format_layout.addWidget(lbl_format)
        format_layout.addWidget(self.cmb_format)
        format_layout.addStretch()
        
        options_layout.addLayout(format_layout)
        
        # Row 2: Output directory option
        dir_layout = QHBoxLayout()
        
        self.chk_same_folder = QCheckBox("Export to same folder as source")
        self.chk_same_folder.setChecked(False)  # Default: export to drive root/converted_images
        self.chk_same_folder.setToolTip(
            "If checked, output files will be saved in the same folder as the source files.\n"
            "If unchecked (default), output files will be saved to drive root\\converted_images folder."
        )
        
        dir_layout.addWidget(self.chk_same_folder)
        dir_layout.addStretch()
        
        options_layout.addLayout(dir_layout)
        
        # Add the options frame to custom layout
        self.custom_layout.addWidget(options_frame)

    def _show_ffmpeg_warning(self):
        """Display a warning when ffmpeg is not found in PATH."""
        warning_frame = QFrame()
        warning_frame.setObjectName("warningFrame")
        warning_frame.setStyleSheet("""
            #warningFrame {
                background-color: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        warning_layout = QVBoxLayout(warning_frame)
        
        title_label = QLabel("⚠️ FFmpeg Not Found")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #856404;
        """)
        
        message_label = QLabel(
            "FFmpeg is required for image conversion but was not found in your system PATH.\n\n"
            "To use this feature:\n"
            "1. Download FFmpeg from https://ffmpeg.org/download.html\n"
            "2. Install or extract it to a folder\n"
            "3. Add the 'bin' folder to your system PATH environment variable\n"
            "4. Restart this application"
        )
        message_label.setStyleSheet("color: #856404;")
        message_label.setWordWrap(True)
        
        warning_layout.addWidget(title_label)
        warning_layout.addWidget(message_label)
        
        self.custom_layout.addWidget(warning_frame)
        
        # Disable controls
        self.btn_add_files.setEnabled(False)
        self.btn_add_folder.setEnabled(False)
        self.btn_run.setEnabled(False)
        self.file_list.setEnabled(False)

    def get_file_filter(self):
        return IMAGE_FILTER

    def run_process(self):
        if not self.ffmpeg_available:
            QMessageBox.warning(
                self, 
                "FFmpeg Not Found",
                "FFmpeg is not available in your system PATH.\n"
                "Please install FFmpeg and add it to your PATH to use this feature."
            )
            return
        
        files = self.file_list.get_all_files()
        if not files:
            return

        # Get selected output format
        output_format = self.cmb_format.currentData()
        same_folder = self.chk_same_folder.isChecked()
        
        jobs = []
        for f in files:
            job = self.logic.get_image_conversion_command(f, output_format, same_folder)
            jobs.append(job)
            
        self.start_worker(jobs)
