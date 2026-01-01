from .base import BaseTab
from ...core.utils import VIDEO_FILTER
from ...core.logic import MkvLogic
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QSpinBox, QGroupBox, QGridLayout, QFrame, QSizePolicy, QWidget
from PyQt6.QtCore import Qt

class CropTab(BaseTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = MkvLogic()

    def create_spinbox(self):
        spinbox = QSpinBox()
        spinbox.setRange(0, 500)
        spinbox.setObjectName("cropInput")
        spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return spinbox

    def init_ui(self):
        super().init_ui()
        
        # Main Layout for this tab
        # We use a central container to hold the crop UI to keep it centered and sized effectively
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 1. Title / Instruction
        lbl_title = QLabel("Crop Margins")
        lbl_title.setObjectName("h2") # Assuming we might have header styles, or just use default
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(lbl_title)
        
        # 2. Compact Grid Layout (No big visualizer)
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create Inputs
        self.spin_top = self.create_spinbox()
        self.spin_bottom = self.create_spinbox()
        self.spin_left = self.create_spinbox()
        self.spin_right = self.create_spinbox()
        
        # Helper to create label+spinbox container
        def create_field(label_text, spinbox):
            vbox = QVBoxLayout()
            vbox.setSpacing(2)
            vbox.addWidget(QLabel(label_text), alignment=Qt.AlignmentFlag.AlignCenter)
            vbox.addWidget(spinbox, alignment=Qt.AlignmentFlag.AlignCenter)
            return vbox

        # Layout:
        #      [Top]
        # [Left]   [Right]
        #     [Bottom]
        
        # Row 0: Top
        grid.addLayout(create_field("Top", self.spin_top), 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        
        # Row 1: Left & Right
        grid.addLayout(create_field("Left", self.spin_left), 1, 0)
        grid.addLayout(create_field("Right", self.spin_right), 1, 1)
        
        # Row 2: Bottom
        grid.addLayout(create_field("Bottom", self.spin_bottom), 2, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addLayout(grid)
        
        # Add the container to the BaseTab's custom layout
        self.custom_layout.addWidget(container)

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
