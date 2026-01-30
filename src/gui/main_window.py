"""
Main application window for Nimar PDF Converter - PDF viewer removed
"""

import os
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QStatusBar, QLabel, QFrame, QPushButton,
    QMessageBox, QFileDialog, QRadioButton, QButtonGroup,
    QCheckBox, QProgressBar
)
from PySide6.QtCore import Qt, QSize, QThread, Signal
from PySide6.QtGui import QAction, QIcon

from gui.file_list_widget import FileListWidget
from gui.setup_dialog import SetupDialog
from gui.save_dialog import SaveDialog
from conversion.converter import DocumentConverter
from pdf_ops.merger import PDFMerger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nimar PDF Converter - निमाड़ पीडीएफ कंवर्टर")
        self.setMinimumSize(QSize(800, 600))
        
        # Initialize converters
        self.converter = DocumentConverter()
        self.pdf_merger = PDFMerger()
        
        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
        
    def setup_ui(self):
        """Setup the main user interface"""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Title label
        title_label = QLabel("Document to PDF Converter")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # File list widget
        self.file_list = FileListWidget(self)
        main_layout.addWidget(self.file_list)
        
        # Control buttons area
        control_frame = QFrame()
        control_layout = QHBoxLayout(control_frame)
        
        # File management buttons
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.clicked.connect(self.add_files)
        control_layout.addWidget(self.add_files_btn)
        
        self.remove_file_btn = QPushButton("Remove Selected")
        self.remove_file_btn.clicked.connect(self.remove_selected_file)
        control_layout.addWidget(self.remove_file_btn)
        
        # Arrange buttons
        control_layout.addWidget(QLabel("Arrange:"))
        self.up_btn = QPushButton("Up")
        self.up_btn.clicked.connect(self.move_file_up)
        control_layout.addWidget(self.up_btn)
        
        self.down_btn = QPushButton("Down")
        self.down_btn.clicked.connect(self.move_file_down)
        control_layout.addWidget(self.down_btn)
        
        control_layout.addStretch()
        
        main_layout.addWidget(control_frame)
        
        # Conversion options
        options_frame = QFrame()
        options_layout = QHBoxLayout(options_frame)
        
        # Output format radio buttons
        self.output_group = QButtonGroup()
        self.individual_radio = QRadioButton("Individual PDFs")
        self.individual_radio.setChecked(True)
        self.merged_radio = QRadioButton("Merged PDF")
        
        self.output_group.addButton(self.individual_radio, 0)
        self.output_group.addButton(self.merged_radio, 1)
        
        options_layout.addWidget(QLabel("Output:"))
        options_layout.addWidget(self.individual_radio)
        options_layout.addWidget(self.merged_radio)
        options_layout.addStretch()
        
        main_layout.addWidget(options_frame)
        
        # Convert button
        convert_frame = QFrame()
        convert_layout = QHBoxLayout(convert_frame)
        
        self.convert_btn = QPushButton("Convert to PDF")
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.convert_btn.clicked.connect(self.convert_files)
        convert_layout.addWidget(self.convert_btn)
        
        convert_layout.addStretch()
        
        main_layout.addWidget(convert_frame)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        self.setCentralWidget(central_widget)
        
    def setup_menu(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        add_files_action = QAction("Add Files", self)
        add_files_action.triggered.connect(self.add_files)
        file_menu.addAction(add_files_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        setup_libreoffice_action = QAction("Setup LibreOffice", self)
        setup_libreoffice_action.triggered.connect(self.setup_libreoffice)
        tools_menu.addAction(setup_libreoffice_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_statusbar(self):
        """Setup the status bar"""
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def add_files(self):
        """Handle file addition"""
        self.file_list.add_files()
        
    def remove_selected_file(self):
        """Remove selected file from list"""
        current_item = self.file_list.currentItem()
        if current_item:
            self.file_list.takeItem(self.file_list.row(current_item))
        
    def move_file_up(self):
        """Move selected file up in list"""
        self.file_list.move_item_up()
        
    def move_file_down(self):
        """Move selected file down in list"""
        self.file_list.move_item_down()
        
    def convert_files(self):
        """Convert files to PDF"""
        files = self.file_list.get_file_list()
        
        if not files:
            QMessageBox.warning(self, "No Files", "Please add files to convert.")
            return
        
        # Show save dialog
        save_dialog = SaveDialog(self)
        
        # Connect to appropriate method based on selection
        if self.individual_radio.isChecked():
            save_dialog.save_requested.connect(self._perform_individual_conversion)
        else:
            save_dialog.save_requested.connect(self._perform_merge_conversion)
            
        save_dialog.exec()
        
    def _perform_individual_conversion(self, output_dir: str, filename_base: str, overwrite_all: bool):
        """Perform the actual individual file conversion"""
        files = self.file_list.get_file_list()
        
        if not files:
            QMessageBox.warning(self, "No Files", "Please add files to convert.")
            return
        
        # Setup progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(files))
        self.progress_bar.setValue(0)
        
        success_count = 0
        failed_files = []
        
        try:
            for i, file_path in enumerate(files):
                success, message = self.converter.convert_to_pdf(file_path, output_dir)
                if success:
                    success_count += 1
                else:
                    failed_files.append(Path(file_path).name)
                    print(f"Failed to convert {file_path}: {message}")
                
                self.progress_bar.setValue(i + 1)
            
            # Show results
            if failed_files:
                QMessageBox.warning(
                    self, "Conversion Complete with Issues",
                    f"Successfully converted {success_count}/{len(files)} files.\n\n"
                    f"Failed files: {', '.join(failed_files)}"
                )
            else:
                QMessageBox.information(
                    self, "Conversion Complete",
                    f"Successfully converted {success_count}/{len(files)} files individually."
                )
                
        finally:
            self.progress_bar.setVisible(False)
        
    def _perform_merge_conversion(self, output_dir: str, filename_base: str, overwrite_all: bool):
        """Perform the actual merge conversion"""
        files = self.file_list.get_file_list()
        
        if not files:
            QMessageBox.warning(self, "No Files", "Please add files to convert.")
            return
        
        # Setup progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(files) * 2)  # Convert + merge
        self.progress_bar.setValue(0)
        
        try:
            # First convert all files to PDF if needed
            pdf_files = []
            temp_pdf_paths = []
            
            for i, file_path in enumerate(files):
                if file_path.lower().endswith('.pdf'):
                    pdf_files.append(file_path)
                else:
                    success, pdf_path = self.converter.convert_to_pdf(file_path, output_dir)
                    if success and pdf_path:
                        pdf_files.append(pdf_path)
                        temp_pdf_paths.append(pdf_path)
                    else:
                        raise Exception(f"Failed to convert {file_path}")
                
                self.progress_bar.setValue(i + 1)
            
            if len(pdf_files) < 2:
                raise Exception("Need at least 2 files to merge")
            
            # Create output path
            if filename_base.endswith('.pdf'):
                filename_base = filename_base[:-4]
            
            output_path = os.path.join(output_dir, f"{filename_base}_merged.pdf")
            
            # Check for overwrite
            if not overwrite_all and os.path.exists(output_path):
                reply = QMessageBox.warning(
                    self, "File Exists",
                    f"The merged file '{os.path.basename(output_path)}' already exists.\n\nDo you want to overwrite it?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply != QMessageBox.StandardButton.Yes:
                    return
            
            # Merge PDFs
            success, message = self.pdf_merger.merge_pdfs(pdf_files, output_path)
            
            self.progress_bar.setValue(len(pdf_files) + 1)
            
            if success:
                QMessageBox.information(
                    self, "Merge Complete",
                    f"Successfully merged {len(pdf_files)} files into {os.path.basename(output_path)}"
                )
            else:
                raise Exception(message)
                
        finally:
            # Clean up temporary files
            for temp_file in temp_pdf_paths:
                try:
                    if os.path.exists(temp_file) and temp_file not in files:
                        os.remove(temp_file)
                except:
                    pass
            
            self.progress_bar.setVisible(False)
        
    def setup_libreoffice(self):
        """Handle LibreOffice setup"""
        dialog = SetupDialog(self)
        dialog.exec()
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About Nimar PDF Converter",
            "Nimar PDF Converter v1.0\n\n"
            "A simple fast and useful tool to facilitate conversion of documents on the go.\n\n"
            "Supported formats:\n"
            "• Office documents (.doc, .docx, .xls, .xlsx, .ppt, .pptx)\n"
            "• OpenDocument formats (.odt, .ods, .odp)\n"
            "• Image files (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .tif, .webp, .ico)\n"
            "• Text files (.txt, .csv, .xml, .md, .html)\n"
            "• PDF files (for merging)\n"
        )
        
    def _check_converter_status(self):
        """Check if required converters are available"""
        status = self.converter.get_converter_status()
        
        if not status['libreoffice']:
            self.status_bar.showMessage("Warning: LibreOffice not available - Office document conversion disabled")
        else:
            self.status_bar.showMessage("Ready - All converters available")