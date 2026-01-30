"""
File list widget for managing uploaded files with drag-drop support
"""

import os
from pathlib import Path
from typing import List

from PySide6.QtWidgets import (
    QListWidget, QListWidgetItem, QFileDialog, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor, QFont

from conversion.converter import DocumentConverter

class FileListItem(QListWidgetItem):
    """Custom list item for file display"""
    
    def __init__(self, file_path: str, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.file_info = Path(file_path)
        
        # Set display text and tooltip
        self.setText(self.file_info.name)
        self.setToolTip(f"{self.file_info.name}\nPath: {file_path}\nSize: {self._get_file_size()}")
        
        # Set icon based on file type
        self.setIcon(self._get_file_icon())
        
        # Store user data
        self.setData(Qt.ItemDataRole.UserRole, file_path)
    
    def _get_file_size(self) -> str:
        """Get human-readable file size"""
        try:
            size = self.file_info.stat().st_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Unknown"
    
    def _get_file_icon(self) -> QIcon:
        """Get icon based on file extension"""
        ext = self.file_info.suffix.lower()
        
        # Simple text-based icons for now
        if ext in ['.doc', '.docx']:
            return self._create_text_icon("DOC", "#2E74B5")
        elif ext in ['.xls', '.xlsx']:
            return self._create_text_icon("XLS", "#217346")
        elif ext in ['.ppt', '.pptx']:
            return self._create_text_icon("PPT", "#D24726")
        elif ext == '.pdf':
            return self._create_text_icon("PDF", "#E3120B")
        elif ext in ['.odt', '.ods', '.odp']:
            return self._create_text_icon("ODF", "#FF6600")
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico']:
            return self._create_text_icon("IMG", "#3498DB")
        else:
            return self._create_text_icon("FILE", "#666666")
    
    def _create_text_icon(self, text: str, color: str) -> QIcon:
        """Create a simple text-based icon"""
        pixmap = QPixmap(48, 48)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        # Draw a simple colored rectangle with text
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.setBrush(QColor(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(4, 4, 40, 40, 4, 4)
        
        # Text
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)
        
        painter.end()
        return QIcon(pixmap)

class FileListWidget(QListWidget):
    """List widget with drag-drop support for files"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Setup widget properties
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setAlternatingRowColors(True)
        
        # Initialize converter
        self.converter = DocumentConverter()
        self.supported_formats = self.converter.get_supported_extensions()
        
        # Setup context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        
        # Header text
        self._update_placeholder()
    
    def _update_placeholder(self):
        """Update placeholder text based on item count"""
        if self.count() == 0:
            self.setStyleSheet("""
                QListWidget {
                    border: 2px dashed #bdc3c7;
                    border-radius: 10px;
                    background-color: #f8f9fa;
                    min-height: 200px;
                }
            """)
        else:
            self.setStyleSheet("""
                QListWidget {
                    border: 2px solid #bdc3c7;
                    border-radius: 10px;
                    background-color: white;
                    min-height: 200px;
                }
            """)
    
    def add_files(self):
        """Open file dialog to add files"""
        # Create filter string
        format_str = ";;".join([
            f"Office Documents (*.doc *.docx *.xls *.xlsx *.ppt *.pptx *.odt *.ods *.odp)",
            f"Image Files (*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp *.ico)",
            f"Text Files (*.txt *.csv *.xml *.md *.html *.htm)",
            f"PDF Files (*.pdf)",
            f"All Supported Files (*{' *'.join(self.supported_formats)})"
        ])
        
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files to Convert",
            "",
            format_str
        )
        
        if files:
            self._add_files_to_list(files)
    
    def _add_files_to_list(self, file_paths: List[str]):
        """Add files to the list, filtering for supported formats"""
        added_count = 0
        
        for file_path in file_paths:
            if self.converter.is_supported(file_path):
                # Check for duplicates
                if not self._file_already_exists(file_path):
                    item = FileListItem(file_path, self)
                    self.addItem(item)
                    added_count += 1
            else:
                # Show warning for unsupported files
                QMessageBox.warning(
                    self,
                    "Unsupported Format",
                    f"File {Path(file_path).name} is not supported and will be skipped."
                )
        
        self._update_placeholder()
        print(f"Added {added_count} files")  # Simple status update
    
    def _file_already_exists(self, file_path: str) -> bool:
        """Check if file is already in the list"""
        for i in range(self.count()):
            item = self.item(i)
            if hasattr(item, 'file_path') and item.file_path == file_path:
                return True
        return False
    
    def _show_context_menu(self, position):
        """Show context menu for file items"""
        item = self.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        
        remove_action = QAction("Remove", self)
        remove_action.triggered.connect(lambda: self._remove_item(item))
        menu.addAction(remove_action)
        
        menu.exec_(self.mapToGlobal(position))
    
    def _remove_item(self, item):
        """Remove item from list"""
        row = self.row(item)
        self.takeItem(row)
        self._update_placeholder()
        print("File removed")  # Simple status update
    
    # Drag and Drop methods
    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)
    
    def dragMoveEvent(self, event):
        """Handle drag move event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)
    
    def dropEvent(self, event):
        """Handle drop event"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            file_paths = []
            
            for url in urls:
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if os.path.isfile(file_path):
                        file_paths.append(file_path)
            
            if file_paths:
                self._add_files_to_list(file_paths)
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            super().dropEvent(event)
    
    def get_file_list(self) -> List[str]:
        """Get list of all file paths"""
        file_paths = []
        for i in range(self.count()):
            item = self.item(i)
            if hasattr(item, 'file_path'):
                file_paths.append(item.file_path)
        return file_paths
    
    def move_item_up(self):
        """Move selected item up"""
        current_row = self.currentRow()
        if current_row > 0:
            item = self.takeItem(current_row)
            self.insertItem(current_row - 1, item)
            self.setCurrentRow(current_row - 1)
    
    def move_item_down(self):
        """Move selected item down"""
        current_row = self.currentRow()
        if current_row < self.count() - 1:
            item = self.takeItem(current_row)
            self.insertItem(current_row + 1, item)
            self.setCurrentRow(current_row + 1)