"""
Setup dialog for LibreOffice installation guidance
"""

import sys
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QProgressBar, QMessageBox, QFrame, QGridLayout,
    QGroupBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

from conversion.dependency_check import LibreOfficeChecker

class SetupDialog(QDialog):
    """Dialog for checking and guiding LibreOffice installation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("LibreOffice Setup")
        self.setMinimumSize(600, 500)
        self.setModal(True)
        
        self.checker = LibreOfficeChecker()
        self.setup_ui()
        self.check_status()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("LibreOffice Setup")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Status section
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Checking LibreOffice status...")
        status_layout.addWidget(self.status_label)
        
        self.version_label = QLabel("")
        status_layout.addWidget(self.version_label)
        
        layout.addWidget(status_group)
        
        # Instructions section
        instructions_group = QGroupBox("Installation Instructions")
        instructions_layout = QVBoxLayout(instructions_group)
        
        self.instructions_text = QTextEdit()
        self.instructions_text.setReadOnly(True)
        self.instructions_text.setMaximumHeight(200)
        instructions_layout.addWidget(self.instructions_text)
        
        layout.addWidget(instructions_group)
        
        # Download links section
        links_group = QGroupBox("Download Links")
        links_layout = QGridLayout(links_group)
        
        self.download_buttons = []
        links = self.checker.get_download_links()
        
        for i, (label, url) in enumerate(links):
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, u=url: self._open_url(u))
            links_layout.addWidget(btn, i // 2, i % 2)
            self.download_buttons.append(btn)
        
        layout.addWidget(links_group)
        
        # Test section
        test_group = QGroupBox("Test Conversion")
        test_layout = QVBoxLayout(test_group)
        
        self.test_button = QPushButton("Test LibreOffice Conversion")
        self.test_button.clicked.connect(self.test_conversion)
        test_layout.addWidget(self.test_button)
        
        self.test_progress = QProgressBar()
        self.test_progress.setVisible(False)
        test_layout.addWidget(self.test_progress)
        
        self.test_result = QLabel("")
        test_layout.addWidget(self.test_result)
        
        layout.addWidget(test_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Refresh Status")
        self.refresh_button.clicked.connect(self.check_status)
        button_layout.addWidget(self.refresh_button)
        
        button_layout.addStretch()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
    
    def check_status(self):
        """Check and display LibreOffice status"""
        if self.checker.is_available():
            self.status_label.setText("✅ LibreOffice is installed and available")
            self.status_label.setStyleSheet("color: green;")
            
            version = self.checker.get_version()
            self.version_label.setText(f"Version: {version}")
            
            self.test_button.setEnabled(True)
        else:
            self.status_label.setText("❌ LibreOffice not found")
            self.status_label.setStyleSheet("color: red;")
            
            self.version_label.setText("Version: Not installed")
            self.instructions_text.setText(self.checker.get_install_instructions())
            self.test_button.setEnabled(False)
    
    def test_conversion(self):
        """Test LibreOffice conversion functionality"""
        self.test_progress.setVisible(True)
        self.test_progress.setRange(0, 0)  # Indeterminate progress
        self.test_result.setText("Testing conversion...")
        self.test_button.setEnabled(False)
        
        # Perform test in background thread
        success, message = self.checker.test_conversion()
        
        self.test_progress.setVisible(False)
        
        if success:
            self.test_result.setText(f"✅ {message}")
            self.test_result.setStyleSheet("color: green;")
        else:
            self.test_result.setText(f"❌ {message}")
            self.test_result.setStyleSheet("color: red;")
        
        self.test_button.setEnabled(True)
    
    def open_download_page(self):
        """Open LibreOffice download page"""
        self.checker.open_download_page()
    
    def _open_url(self, url):
        """Open URL in browser"""
        import webbrowser
        webbrowser.open(url)