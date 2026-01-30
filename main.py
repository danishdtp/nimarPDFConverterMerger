#!/usr/bin/env python3
"""
Nimar PDF Converter - निमाड़ पीडीएफ कंवर्टर एवं मर्ज साॅफ़टवेयर
A simple fast and useful tool to facilitate conversion of documents on the go.
Supports multiple files to be concatenated into single PDF or individual PDFs.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLocale
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Nimar PDF Converter")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Nimar Software")
    
    # Load translation if available
    translator = QTranslator()
    if translator.load(QLocale(), "translations", "_", "src/resources/translations"):
        app.installTranslator(translator)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()