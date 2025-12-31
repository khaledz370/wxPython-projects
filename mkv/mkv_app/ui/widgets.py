import os
from PyQt6.QtWidgets import (
    QListWidget, QListWidgetItem, QAbstractItemView, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal

class FileListWidget(QListWidget):
    """
    A list widget that supports files, drag & drop, and checkboxes for selection.
    """
    files_dropped = pyqtSignal(list)
    selection_changed = pyqtSignal()

    def __init__(self, allowed_extensions=None):
        super().__init__()
        self.allowed_extensions = allowed_extensions  # List of strings, e.g., ['.mkv', '.mp4']
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        self.setAcceptDrops(True)
        # We use strict checkboxes if the user wants to explicitly check items to delete
        # But standard QListWidget selection is usually better for 'Select to Delete'.
        # However, to be faithful to the original which used CheckListBox:
        self.itemChanged.connect(self.on_item_changed)

    def dragEnterEvent(self, event):
        print("DEBUG: FileListWidget Drag Enter")
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        print("DEBUG: FileListWidget Drop Event")
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            file_paths = []
            for url in urls:
                path = url.toLocalFile()
                if os.path.isdir(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            if self.is_allowed(full_path):
                                file_paths.append(full_path)
                else:
                    if self.is_allowed(path):
                        file_paths.append(path)
            
            self.add_files(file_paths)
            self.files_dropped.emit(file_paths)

    def is_allowed(self, path):
        if not self.allowed_extensions:
            return True
        return any(path.lower().endswith(ext.lower()) for ext in self.allowed_extensions)

    def add_files(self, paths):
        existing_paths = {self.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.count())}
        new_paths = [p for p in paths if p not in existing_paths]
        new_paths.sort()
        
        for path in new_paths:
            item = QListWidgetItem(os.path.basename(path))
            item.setData(Qt.ItemDataRole.UserRole, path)
            item.setToolTip(path)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.addItem(item)
            
    def get_all_files(self):
        """Returns full paths of all files in the list."""
        return [self.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.count())]

    def get_checked_files(self):
        """Returns full paths of checked files."""
        return [
            self.item(i).data(Qt.ItemDataRole.UserRole) 
            for i in range(self.count()) 
            if self.item(i).checkState() == Qt.CheckState.Checked
        ]

    def remove_checked_items(self):
        """Removes all checked items from the list."""
        for i in range(self.count() - 1, -1, -1):
            if self.item(i).checkState() == Qt.CheckState.Checked:
                self.takeItem(i)

    def check_all(self, checked=True):
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        for i in range(self.count()):
            self.item(i).setCheckState(state)

    def on_item_changed(self, item):
        self.selection_changed.emit()
