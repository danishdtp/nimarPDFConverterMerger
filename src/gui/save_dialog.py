"""
Custom save dialog with overwrite warnings for Nimar PDF Converter
"""

import os
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QMessageBox, QCheckBox,
    QGroupBox, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class SaveDialog(QDialog):
    """Enhanced save dialog with overwrite warnings"""
    
    # Signal for save decision
    save_requested = Signal(str, str, bool)  # directory, filename_base, overwrite_all
    
    def __init__(self, parent=None, default_filename="converted_files", output_dir=""):
        super().__init__(parent)
        self.setWindowTitle("Save PDF Files")
        self.setMinimumSize(500, 400)
        self.setModal(True)
        
        # Initialize variables
        self.output_dir = output_dir
        self.default_filename = default_filename
        self.overwrite_all = False
        self.show_preview = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Directory selection
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Output Directory:"))
        
        self.dir_edit = QLineEdit(self.output_dir)
        self.dir_edit.setReadOnly(True)
        dir_layout.addWidget(self.dir_edit)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.browse_btn)
        
        layout.addLayout(dir_layout)
        
        # Filename base
        filename_layout = QHBoxLayout()
        filename_layout.addWidget(QLabel("Base Filename:"))
        
        self.filename_edit = QLineEdit(self.default_filename)
        self.filename_edit.setPlaceholderText("Enter base filename...")
        filename_layout.addWidget(self.filename_edit)
        
        layout.addLayout(filename_layout)
        
        # Overwrite options
        options_group = QGroupBox("File Handling Options")
        options_layout = QVBoxLayout(options_group)
        
        self.overwrite_all_cb = QCheckBox("Overwrite existing files without asking")
        self.overwrite_all_cb.toggled.connect(self.toggle_overwrite_all)
        options_layout.addWidget(self.overwrite_all_cb)
        
        self.show_preview_cb = QCheckBox("Show files that will be overwritten")
        self.show_preview_cb.toggled.connect(self.toggle_preview)
        options_layout.addWidget(self.show_preview_cb)
        
        layout.addWidget(options_group)
        
        # Preview area (initially hidden)
        self.preview_widget = QListWidget()
        self.preview_widget.setMaximumHeight(100)
        self.preview_widget.setVisible(False)
        layout.addWidget(self.preview_widget)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
    def browse_directory(self):
        """Browse for output directory"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", self.output_dir
        )
        if directory:
            self.output_dir = directory
            self.dir_edit.setText(directory)
            self.update_preview()
    
    def toggle_overwrite_all(self, checked):
        """Toggle overwrite all option"""
        self.overwrite_all = checked
        self.update_preview()
    
    def toggle_preview(self, checked):
        """Toggle file preview"""
        self.show_preview = checked
        self.preview_widget.setVisible(checked)
        self.update_preview()
    
    def update_preview(self):
        """Update the preview of files that will be affected"""
        self.preview_widget.clear()
        
        if not self.output_dir or not self.show_preview:
            return
        
        output_path = Path(self.output_dir)
        
        # Check for existing files that would be overwritten
        filename_base = self.filename_edit.text().strip() or self.default_filename
        
        if filename_base.endswith('.pdf'):
            filename_base = filename_base[:-4]
        
        # Check individual files
        existing_files = []
        
        # Check for individual converted files
        individual_pattern = f"{filename_base}_converted.pdf"
        individual_path = output_path / individual_pattern
        if individual_path.exists():
            existing_files.append(individual_pattern)
        
        # Check for merged file
        merged_pattern = f"{filename_base}_merged.pdf"
        merged_path = output_path / merged_pattern
        if merged_path.exists():
            existing_files.append(merged_pattern)
        
        if existing_files:
            if self.overwrite_all:
                # Show files that will be overwritten
                for file in existing_files:
                    item = QListWidgetItem(f"📁 {file} (will be overwritten)")
                    item.setFont(QFont("Arial", 9))
                    self.preview_widget.addItem(item)
            else:
                # Show warning for files that exist
                for file in existing_files:
                    item = QListWidgetItem(f"⚠️ {file} (already exists)")
                    item.setFont(QFont("Arial", 9))
                    self.preview_widget.addItem(item)
        else:
            # No conflicts
            item = QListWidgetItem("✅ No files will be overwritten")
            item.setFont(QFont("Arial", 9))
            self.preview_widget.addItem(item)
    
    def accept(self):
        """Handle save acceptance"""
        filename_base = self.filename_edit.text().strip() or self.default_filename
        
        if not filename_base.endswith('.pdf'):
            filename_base += '.pdf'
        
        # Final validation
        output_path = Path(self.output_dir) / filename_base
        
        if not self.overwrite_all and output_path.exists():
            reply = QMessageBox.warning(
                self,
                "File Exists",
                f"The file '{filename_base}' already exists.\n\nDo you want to overwrite it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return  # User cancelled
        
        # Emit save signal
        self.save_requested.emit(self.output_dir, filename_base, self.overwrite_all)
        super().accept()
    
    def get_save_info(self):
        """Get save dialog information"""
        return {
            'directory': self.output_dir,
            'filename_base': self.filename_edit.text().strip() or self.default_filename,
            'overwrite_all': self.overwrite_all
        }