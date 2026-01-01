import sys
import os
from PyQt6.QtWidgets import QApplication
from .ui.main_window import MainWindow

def create_app():
    app = QApplication(sys.argv)
    
    # Optional: Load fonts or other global initialization here
    # Load Stylesheet and Icon Globally
    from PyQt6.QtGui import QIcon
    
    def resolve_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            # In Dev mode: mkv_app/app.py -> parent is mkv_app -> parent is root
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        return os.path.join(base_path, relative_path)

    # Set App Icon
    # We expect mkv.ico to be at the root of the bundle or source
    icon_path = resolve_path("mkv.ico")
    if os.path.exists(icon_path):
         app.setWindowIcon(QIcon(icon_path))
    else:
        print(f"DEBUG: Icon not found at {icon_path}")

    # Theme Management
    from .ui.theme import ThemeManager, AppTheme
    
    # Apply Dark Theme by default
    ThemeManager.apply_theme(app, AppTheme.DARK)
    
    # We no longer load 'styles.qss' manually, but we keep the file existence check for legacy reasons if needed, 
    # or just remove it. The ThemeManager generates it dynamically.
    print("Theme applied: Dark Mode")

    window = MainWindow()
    window.show()
    
    return app, window
