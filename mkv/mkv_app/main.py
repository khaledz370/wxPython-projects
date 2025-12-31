import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QLockFile, QDir
from mkv_app.app import create_app

def main():
    # Single Instance Logic
    lock_file_path = os.path.join(QDir.tempPath(), 'mkv_batch_app.lock')
    lock_file = QLockFile(lock_file_path)
    
    # Try to lock, wait 100ms
    if not lock_file.tryLock(100):
        # Already running
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Already Running", "Another instance of MKV Batch App is already running.")
        sys.exit(1)

    # Validating taskbar icon on Windows
    import ctypes
    myappid = 'mkvbatchapp.v2.0' # arbitrary string
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    app, window = create_app()
    
    exit_code = app.exec()
    
    # Cleanup
    lock_file.unlock()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
