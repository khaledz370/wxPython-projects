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

    # Set Stylesheet
    # We expect mkv_app/ui/styles.qss. 
    # In PyInstaller with --add-data "mkv_app/ui/styles.qss;mkv_app/ui", it will be at root/mkv_app/ui/styles.qss
    style_path = resolve_path(os.path.join("mkv_app", "ui", "styles.qss"))
    
    # Fallback for dev mode where 'mkv_app' is the folder we are in, but resolve_path goes to root
    if not os.path.exists(style_path):
         style_path = resolve_path(os.path.join("mkv_app", "ui", "styles.qss")) 

    if os.path.exists(style_path):
        print(f"Loading stylesheet from: {style_path}")
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"ERROR: Stylesheet not found at {style_path}")

    window = MainWindow()
    window.show()
    
    return app, window
