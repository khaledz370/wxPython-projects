from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMenu, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from .tabs.conversion import ToMkvTab, ToAudioTab
from .tabs.crop import CropTab
from .tabs.options import OptionsTab
from .tabs.translate import TranslateTab
from .tabs.image_conversion import ImageConversionTab
from .dialogs import SettingsDialog
from ..core.settings import AppSettings
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MKV Batch App v2.0")
        self.resize(900, 650)
        
        # Icon
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "mkv.ico"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.tab_mkv = ToMkvTab(self)
        self.tab_audio = ToAudioTab(self)
        self.tab_crop = CropTab(self)
        self.tab_options = OptionsTab(self)
        self.tab_translate = TranslateTab(self)
        self.tab_image_convert = ImageConversionTab(self)
        
        self.tabs.addTab(self.tab_mkv, "To MKV")
        self.tabs.addTab(self.tab_audio, "To Audio")
        self.tabs.addTab(self.tab_crop, "Crop")
        self.tabs.addTab(self.tab_options, "Options")
        self.tabs.addTab(self.tab_translate, "Translate")
        self.tabs.addTab(self.tab_image_convert, "Image Convert")
        
        # Menu Bar
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("&File")
        
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.open_settings)
        file_menu.addAction(settings_action)
        
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()
        # Potentially reload settings in tabs if needed?

    def show_about(self):
        QMessageBox.about(self, "About MKV Batch App", 
                          "MKV Batch App v2.0\n\n"
                          "A modern PyQt6 application for batch processing MKV files.\n"
                          "Migrated from wxPython with love.")

    def closeEvent(self, event):
        """Ensure all processes are aborted on close."""
        # Iterate through all tabs and abort if running
        tabs = [self.tab_mkv, self.tab_audio, self.tab_crop, self.tab_options, self.tab_translate, self.tab_image_convert]
        for tab in tabs:
            if hasattr(tab, 'worker') and tab.worker is not None:
                print(f"Aborting worker in tab: {tab}")
                tab.abort_process()
                # Optional: Wait a brief moment? The worker kill is async but uses terminate/kill.
        
        event.accept()
