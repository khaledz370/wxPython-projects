from .base import BaseTab
from ...core.utils import VIDEO_FILTER
from ...core.logic import MkvLogic
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSpinBox, QGroupBox, QGridLayout
from PyQt6.QtCore import Qt

class CropTab(BaseTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = MkvLogic()

    def create_spinbox(self):
        spinbox = QSpinBox()
        spinbox.setRange(0, 500)
        return spinbox

    def init_ui(self):
        super().init_ui()
        
        # Crop Controls
        # We use a visual grid for Top, Left, Right, Bottom
        self.grp_crop = QGroupBox("Crop Settings (Pixels)")
        self.grp_crop.setMaximumHeight(200) # Keep it compact
        
        grid = QGridLayout()
        
        # Center the grid content
        grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spin_top = self.create_spinbox()
        self.spin_bottom = self.create_spinbox()
        self.spin_left = self.create_spinbox()
        self.spin_right = self.create_spinbox()
        
        # Layout:
        #       Top
        # Left       Right
        #      Bottom
        
        grid.addWidget(QLabel("Top:"), 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.spin_top, 1, 1)
        
        grid.addWidget(QLabel("Left:"), 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.spin_left, 3, 0)
        
        grid.addWidget(QLabel("Right:"), 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.spin_right, 3, 2)
        
        grid.addWidget(QLabel("Bottom:"), 4, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.spin_bottom, 5, 1)
        
        self.grp_crop.setLayout(grid)
        
        self.custom_layout.addWidget(self.grp_crop)
        # Add stretch to push the box up if needed, though BaseTab handles this
        # self.custom_layout.addStretch()

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
