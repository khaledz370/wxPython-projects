from enum import Enum
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

class AppTheme(Enum):
    DARK = "dark"
    LIGHT = "light"

# Modern Color Palette (Dracula / Nord / VS Code inspired for Dark, Clean Gray for Light)
PALETTE = {
    "dark": {
        "bg_primary": "#1e1e1e",      # Main Window Background
        "bg_secondary": "#252526",    # Sidebar / Tab Bar
        "bg_tertiary": "#2d2d2d",     # Hover states
        "bg_input": "#3c3c3c",        # Input fields
        "border": "#454545",          # Borders
        "text_primary": "#cccccc",    # Main Text
        "text_secondary": "#969696",  # Subtitles / Disabled
        "accent": "#0078d4",          # Primary Action Blue
        "accent_hover": "#2b88d8",
        "danger": "#d83b01",          # Red/Orange for delete/abort
        "danger_hover": "#ea4a1f",
        "success": "#107c10",
        "scroll_handle": "#424242",
        "scroll_bg": "#2e2e2e",
    },
    "light": {
        "bg_primary": "#f3f3f3",
        "bg_secondary": "#e8e8e8",
        "bg_tertiary": "#dcdcdc",
        "bg_input": "#ffffff",
        "border": "#cccccc",
        "text_primary": "#333333",
        "text_secondary": "#666666",
        "accent": "#0067c0",
        "accent_hover": "#0078d4",
        "danger": "#c50f1f",
        "danger_hover": "#d92b2b",
        "success": "#107c10",
        "scroll_handle": "#c1c1c1",
        "scroll_bg": "#f0f0f0",
    }
}

class ThemeManager:
    @staticmethod
    def get_stylesheet(theme: AppTheme = AppTheme.DARK) -> str:
        colors = PALETTE[theme.value]
        
        # We use f-strings to inject colors into the QSS
        qss = f"""
        /* --- Main Window & General --- */
        QMainWindow, QDialog {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
        }}

        QWidget {{
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
            font-size: 14px;
            color: {colors['text_primary']};
            background: transparent;
        }}

        /* --- Tabs --- */
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            background: {colors['bg_primary']};
            top: -1px; /* Align perfectly */
        }}

        QTabBar::tab {{
            background: {colors['bg_secondary']};
            color: {colors['text_secondary']};
            padding: 8px 16px;
            border: 1px solid transparent;
            border-bottom: none;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            font-weight: 500;
        }}

        QTabBar::tab:selected {{
            background: {colors['bg_primary']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
            border-bottom: 2px solid {colors['accent']}; /* Bottom Accent Line */
        }}

        QTabBar::tab:hover {{
            background: {colors['bg_tertiary']};
            color: {colors['text_primary']};
        }}

        /* --- Buttons --- */
        QPushButton {{
            background-color: {colors['bg_secondary']};
            border: 1px solid {colors['border']};
            border-radius: 4px;
            color: {colors['text_primary']};
            padding: 6px 16px;
            font-weight: 500;
        }}
        
        QPushButton:hover {{
            background-color: {colors['bg_tertiary']};
            border-color: {colors['text_secondary']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['border']};
        }}
        
        QPushButton:disabled {{
            background-color: {colors['bg_primary']};
            color: {colors['text_secondary']};
            border: 1px solid {colors['bg_secondary']};
        }}

        /* Primary Action Button */
        QPushButton[class="primary"] {{
            background-color: {colors['accent']};
            color: #ffffff;
            border: 1px solid {colors['accent']};
        }}
        
        QPushButton[class="primary"]:hover {{
            background-color: {colors['accent_hover']};
            border-color: {colors['accent_hover']};
        }}

        /* Danger/Abort Button */
        QPushButton#dangerButton {{
            background-color: {colors['danger']};
            color: white;
            border: 1px solid {colors['danger']};
        }}
        
        QPushButton#dangerButton:hover {{
            background-color: {colors['danger_hover']};
        }}

        /* --- Inputs --- */
        QLineEdit, QSpinBox, QComboBox, QPlainTextEdit {{
            background-color: {colors['bg_input']};
            border: 1px solid {colors['border']};
            border-radius: 4px;
            padding: 6px;
            color: {colors['text_primary']};
            selection-background-color: {colors['accent']};
            selection-color: white;
        }}

        QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
            border: 2px solid {colors['accent']};
            padding: 5px; /* Adjust for thicker border */
        }}
        
        QLineEdit:disabled, QSpinBox:disabled {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_secondary']};
        }}

        /* --- Lists & Trees --- */
        QListWidget, QTreeWidget {{
            background-color: {colors['bg_secondary']};
            border: 1px solid {colors['border']};
            border-radius: 4px;
        }}
        
        QListWidget::item {{
            padding: 6px;
            margin: 2px;
            border-radius: 3px;
        }}
        
        QListWidget::item:selected {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        QListWidget::item:hover {{
            background-color: {colors['bg_tertiary']};
        }}

        /* --- Group Box --- */
        QGroupBox {{
            font-weight: bold;
            border: 1px solid {colors['border']};
            border-radius: 6px;
            margin-top: 24px;
            padding-top: 10px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: {colors['accent']};
            background-color: transparent;
        }}

        /* --- Scrollbars --- */
        QScrollBar:vertical {{
            border: none;
            background: {colors['scroll_bg']};
            width: 10px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {colors['scroll_handle']};
            min-height: 20px;
            border-radius: 5px;
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px; 
        }}

        /* --- Custom Elements (Crop, etc) --- */
        QLabel#h2 {{
            font-size: 18px;
            font-weight: 600;
            color: {colors['text_primary']};
            margin-bottom: 12px;
        }}
        
        QFrame#cropVisualizer {{
            background-color: #000;
            border: 2px solid {colors['border']};
            border-radius: 8px;
        }}
        
        QSpinBox#cropInput {{
            min-width: 60px;
            font-weight: bold;
            background-color: {colors['bg_secondary']};
            border: 1px solid {colors['border']};
        }}
        
        QSpinBox#cropInput:focus {{
            border-color: {colors['accent']};
            background-color: {colors['bg_input']};
        }}
        """
        return qss

    @staticmethod
    def apply_theme(app: QApplication, theme: AppTheme = AppTheme.DARK):
        app.setStyle("Fusion") # Best base style for cross-platform custom branding
        app.setStyleSheet(ThemeManager.get_stylesheet(theme))
