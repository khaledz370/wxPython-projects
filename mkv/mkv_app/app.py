import sys
from PyQt6.QtWidgets import QApplication
from .ui.main_window import MainWindow

def create_app():
    app = QApplication(sys.argv)
    
    # Optional: Load fonts or other global initialization here
    app.setStyle("Fusion")
    
    # Load Stylesheet Globally
    import os
    style_path = os.path.join(os.path.dirname(__file__), "ui", "styles.qss")
    style_path = os.path.abspath(style_path)
    if os.path.exists(style_path):
        print(f"Loading stylesheet from: {style_path}")
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"ERROR: Stylesheet not found at {style_path}")

    window = MainWindow()
    window.show()
    
    return app, window
