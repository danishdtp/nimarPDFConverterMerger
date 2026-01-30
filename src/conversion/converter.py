"""
Main conversion engine that coordinates LibreOffice and Python converters
"""

import os
from pathlib import Path
from typing import List, Tuple, Dict, Optional

from .libreoffice_conv import LibreOfficeConverter
from .python_conv import PythonConverter

class DocumentConverter:
    """Main converter that handles all supported document formats"""
    
    def __init__(self):
        self.libreoffice = LibreOfficeConverter()
        self.python = PythonConverter()
        
    def get_all_supported_formats(self) -> Dict[str, List[str]]:
        """Get all supported formats categorized by converter"""
        return {
            'libreoffice': self.libreoffice.get_supported_formats(),
            'python': self.python.get_supported_formats(),
            'pdf': ['.pdf']  # Special case for PDF merging
        }
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of all supported file extensions"""
        formats = self.get_all_supported_formats()
        all_formats = []
        
        for converter_list in formats.values():
            all_formats.extend(converter_list)
        
        return list(set(all_formats))  # Remove duplicates
    
    def is_supported(self, file_path: str) -> bool:
        """Check if file format is supported"""
        ext = Path(file_path).suffix.lower()
        return ext in self.get_supported_extensions()
    
    def convert_to_pdf(self, input_file: str, output_dir: str) -> Tuple[bool, str]:
        """
        Convert file to PDF using appropriate converter
        
        Args:
            input_file: Path to input file
            output_dir: Directory to save PDF
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not os.path.exists(input_file):
            return False, f"Input file not found: {input_file}"
        
        ext = Path(input_file).suffix.lower()
        
        # Handle PDF files (no conversion needed)
        if ext == '.pdf':
            return True, input_file  # Return original PDF path
        
        # Try LibreOffice first for Office formats
        if ext in self.libreoffice.get_supported_formats():
            if self.libreoffice.is_available():
                return self.libreoffice.convert_to_pdf(input_file, output_dir)
            else:
                return False, f"LibreOffice not available for {ext} file conversion"
        
        # Use Python converter for other formats
        elif ext in self.python.get_supported_formats():
            return self.python.convert_to_pdf(input_file, output_dir)
        
        else:
            return False, f"Unsupported file format: {ext}"
    
    def get_converter_status(self) -> Dict[str, bool]:
        """Get status of available converters"""
        return {
            'libreoffice': self.libreoffice.is_available(),
            'python': True,  # Python converter is always available
        }
    
    def batch_convert_to_pdf(self, file_list: List[str], output_dir: str) -> List[Tuple[str, bool, str]]:
        """
        Convert multiple files to PDF
        
        Args:
            file_list: List of file paths to convert
            output_dir: Directory to save PDFs
            
        Returns:
            List of tuples (file_path, success, message)
        """
        results = []
        
        for file_path in file_list:
            success, message = self.convert_to_pdf(file_path, output_dir)
            results.append((file_path, success, message))
        
        return results