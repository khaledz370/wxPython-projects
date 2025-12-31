import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, 
    QLabel, QProgressBar, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from ..widgets import FileListWidget
from ...core.workers import WorkerThread

class BaseTab(QWidget):
    def __init__(self, parent=None, allowed_extensions=None):
        super().__init__(parent)
        self.allowed_extensions = allowed_extensions
        self.worker = None
        self.setAcceptDrops(True)
        self.init_ui()

    def dragEnterEvent(self, event):
        print("DEBUG: Drag Enter")
        if event.mimeData().hasUrls():
            print("DEBUG: Accepting Drag Enter")
            event.acceptProposedAction()
        else:
            print(f"DEBUG: Drag Ignored. Formats: {event.mimeData().formats()}")
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        print("DEBUG: Drop Event")
        if event.mimeData().hasUrls():
            print("DEBUG: Processing Drop")
            event.acceptProposedAction()
            urls = event.mimeData().urls()
            paths = [url.toLocalFile() for url in urls]
            final_files = []
            for path in paths:
                if os.path.isdir(path):
                     for root, dirs, files in os.walk(path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            if self.file_list.is_allowed(full_path):
                                final_files.append(full_path)
                else:
                    if self.file_list.is_allowed(path):
                        final_files.append(path)
            
            if final_files:
                self.file_list.add_files(final_files)
                self.update_run_button_state()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        
        # 1. Top Controls (Add/Select)
        top_layout = QHBoxLayout()
        
        self.btn_add_files = QPushButton("Add Files")
        self.btn_add_files.clicked.connect(self.add_files)
        
        self.btn_add_folder = QPushButton("Add Folder")
        self.btn_add_folder.clicked.connect(self.add_folder)
        
        self.chk_select_all = QCheckBox("Select All")
        self.chk_select_all.clicked.connect(self.toggle_select_all)
        
        self.btn_remove = QPushButton("Remove Selected")
        self.btn_remove.clicked.connect(self.remove_selected)
        self.btn_remove.setEnabled(False)
        self.btn_remove.setObjectName("dangerButton")
        
        self.btn_clear = QPushButton("Clear List")
        self.btn_clear.clicked.connect(self.clear_list)

        top_layout.addWidget(self.btn_add_files)
        top_layout.addWidget(self.btn_add_folder)
        top_layout.addStretch()
        top_layout.addWidget(self.chk_select_all)
        top_layout.addWidget(self.btn_remove)
        top_layout.addWidget(self.btn_clear)
        
        self.layout.addLayout(top_layout)
        
        # 2. File List
        self.file_list = FileListWidget(self.allowed_extensions)
        self.file_list.selection_changed.connect(self.on_selection_changed)
        # CRITICAL FIX: Update run button when files are dropped onto the list widget directly
        self.file_list.files_dropped.connect(lambda _: self.update_run_button_state())
        self.layout.addWidget(self.file_list)
        
        # 3. Middle / Custom Controls Area (To be populated by subclasses)
        self.custom_layout = QVBoxLayout()
        self.layout.addLayout(self.custom_layout)
        
        # 4. Progress and Run
        bottom_layout = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        
        self.lbl_status = QLabel("Ready")
        
        self.btn_run = QPushButton("Run")
        self.btn_run.clicked.connect(self.run_process)
        self.btn_run.setEnabled(False)
        
        self.btn_abort = QPushButton("Abort")
        self.btn_abort.clicked.connect(self.abort_process)
        self.btn_abort.setEnabled(False)
        self.btn_abort.setObjectName("dangerButton")

        bottom_layout.addWidget(self.progress_bar, 1)
        bottom_layout.addWidget(self.btn_run)
        bottom_layout.addWidget(self.btn_abort)
        
        self.layout.addWidget(self.lbl_status)
        self.layout.addLayout(bottom_layout)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", 
            self.get_file_filter()
        )
        if files:
            self.file_list.add_files(files)
            # Force update of run button state immediately
            self.update_run_button_state()

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            files = []
            for root, _, fs in os.walk(folder):
                for f in fs:
                    if self.file_list.is_allowed(f):
                        files.append(os.path.join(root, f))
            if files:
                self.file_list.add_files(files)
                # Force update of run button state immediately
                self.update_run_button_state()

    def get_file_filter(self):
        return "All Files (*.*)"

    def toggle_select_all(self):
        self.file_list.check_all(self.chk_select_all.isChecked())

    def remove_selected(self):
        self.file_list.remove_checked_items()
        self.update_run_button_state()

    def clear_list(self):
        self.file_list.clear()
        self.update_run_button_state()

    def on_selection_changed(self):
        checked_count = len(self.file_list.get_checked_files())
        self.btn_remove.setEnabled(checked_count > 0)
        self.update_run_button_state()

    def update_run_button_state(self):
        has_items = self.file_list.count() > 0
        print(f"DEBUG: update_run_button_state called. Has Items: {has_items} (Count: {self.file_list.count()})")
        self.btn_run.setEnabled(has_items and not self.worker)

    def run_process(self):
        # To be implemented by subclasses
        pass

    def start_worker(self, jobs):
        if not jobs:
            return

        self.worker = WorkerThread(jobs)
        self.worker.progress.connect(self.on_worker_progress)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.result_ready.connect(self.on_worker_result)
        
        self.btn_run.setEnabled(False)
        self.btn_abort.setEnabled(True)
        self.toggle_inputs(False)
        
        self.worker.start()

    def abort_process(self):
        if self.worker:
            self.worker.abort()
            self.lbl_status.setText("Aborting...")
            self.btn_abort.setEnabled(False)

    def on_worker_progress(self, overall_progress, file_index, status_text):
        self.progress_bar.setValue(overall_progress)
        self.lbl_status.setText(status_text)
        
        # Update list item text if index is valid
        if 0 <= file_index < self.file_list.count():
            item = self.file_list.item(file_index)
            # Extract progress from status text if possible, or just append status
            # status_text format from worker: "Description (X%)"
            # We want to keep original filename and append status.
            original_path = item.data(Qt.ItemDataRole.UserRole)
            filename = os.path.basename(original_path)
            
            # Simple parsing or just use status_text if it contains the filename?
            # Worker sends: "Processing: Description" or "Description (X%)"
            # Let's just set the text to something informative.
            
            # If status_text contains %, use it.
            if "%" in status_text:
                percentage = status_text.split("(")[-1].replace(")", "")
                item.setText(f"{filename} ({percentage})")
            elif "Processing" in status_text:
                 item.setText(f"{filename} (Processing...)")


    def on_worker_result(self, success_count, fail_count, failed_files):
        msg = f"Process complete.\nSuccessful: {success_count}\nFailed: {fail_count}"
        if fail_count > 0:
            msg += f"\nFailed files:\n" + "\n".join([os.path.basename(f) for f in failed_files])
        
        QMessageBox.information(self, "Result", msg)

    def on_worker_finished(self):
        self.worker = None
        self.update_run_button_state()
        self.btn_abort.setEnabled(False)
        self.toggle_inputs(True)
        self.progress_bar.setValue(0)
        self.lbl_status.setText("Ready")
        # Clear list on success? Original app clears list.
        self.file_list.clear()

    def toggle_inputs(self, enabled):
        self.btn_add_files.setEnabled(enabled)
        self.btn_add_folder.setEnabled(enabled)
        self.btn_remove.setEnabled(enabled)
        self.btn_clear.setEnabled(enabled)
        self.file_list.setEnabled(enabled)
