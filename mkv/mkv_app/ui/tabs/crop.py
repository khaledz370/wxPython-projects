from .base import BaseTab
from ...core.utils import VIDEO_FILTER
from ...core.logic import MkvLogic
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSpinBox, QGroupBox, QGridLayout

class CropTab(BaseTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = MkvLogic()

    def init_ui(self):
        super().init_ui()
        
        # Crop Controls
        group = QGroupBox("Crop Settings (Pixels)")
        layout = QGridLayout()
        
        self.spin_top = QSpinBox()
        self.spin_top.setRange(0, 500)
        self.spin_bottom = QSpinBox()
        self.spin_bottom.setRange(0, 500)
        self.spin_left = QSpinBox()
        self.spin_left.setRange(0, 500)
        self.spin_right = QSpinBox()
        self.spin_right.setRange(0, 500)

        # Layout like a frame: Top centered, Left/Right middle, Bottom centered
        layout.addWidget(QLabel("Top:"), 0, 1)
        layout.addWidget(self.spin_top, 1, 1)
        
        layout.addWidget(QLabel("Left:"), 2, 0)
        layout.addWidget(self.spin_left, 3, 0)
        
        layout.addWidget(QLabel("Right:"), 2, 2)
        layout.addWidget(self.spin_right, 3, 2)
        
        layout.addWidget(QLabel("Bottom:"), 4, 1)
        layout.addWidget(self.spin_bottom, 5, 1)
        
        group.setLayout(layout)
        
        # Add to custom area
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(group)
        h_layout.addStretch()
        
        self.custom_layout.addLayout(h_layout)

    def get_file_filter(self):
        return VIDEO_FILTER

    def run_process(self):
        files = self.file_list.get_all_files()
        if not files:
            return

        all_jobs = []
        for f in files:
            # Get list of steps for this file
            steps = self.logic.get_crop_commands(
                f,
                self.spin_top.value(),
                self.spin_left.value(),
                self.spin_right.value(),
                self.spin_bottom.value()
            )
            all_jobs.extend(steps)
            
        self.start_worker(all_jobs)

    def toggle_inputs(self, enabled):
        super().toggle_inputs(enabled)
        self.spin_top.setEnabled(enabled)
        self.spin_bottom.setEnabled(enabled)
        self.spin_left.setEnabled(enabled)
        self.spin_right.setEnabled(enabled)
