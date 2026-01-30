"""
LibreOffice integration for document conversion
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

class LibreOfficeConverter:
    """Handles document conversion using LibreOffice in headless mode"""
    
    def __init__(self):
        self.libreoffice_path = self._find_libreoffice()
        
    def _find_libreoffice(self) -> Optional[str]:
        """Find LibreOffice executable on the system"""
        possible_names = []
        
        if sys.platform.startswith('win'):
            possible_names = [
                'soffice.exe',
                'libreoffice.exe',
                'soffice.com',
                'libreoffice.com'
            ]
            search_paths = [
                os.path.expandvars(r'%PROGRAMFILES%\LibreOffice\program'),
                os.path.expandvars(r'%PROGRAMFILES(X86)%\LibreOffice\program'),
                os.path.expandvars(r'%PROGRAMFILES%\LibreOffice*\program'),
                os.path.expandvars(r'%PROGRAMFILES(X86)%\LibreOffice*\program')
            ]
            
        elif sys.platform.startswith('darwin'):
            possible_names = ['soffice', 'libreoffice']
            search_paths = [
                '/Applications/LibreOffice.app/Contents/MacOS',
                '/opt/homebrew/bin',
                '/usr/local/bin'
            ]
            
        else:  # Linux
            possible_names = ['libreoffice', 'soffice']
            search_paths = [
                '/usr/bin',
                '/usr/local/bin',
                '/opt/libreoffice/program',
                snap_path if os.path.exists(snap_path := '/snap/bin') else None
            ]
        
        # First check system PATH
        for name in possible_names:
            if shutil.which(name):
                return name
        
        # Then check specific paths
        if search_paths:
            for path in search_paths:
                if path and os.path.exists(path):
                    for name in possible_names:
                        exe_path = os.path.join(path, name)
                        if os.path.exists(exe_path):
                            return exe_path
        
        return None
    
    def is_available(self) -> bool:
        """Check if LibreOffice is available"""
        return self.libreoffice_path is not None
    
    def convert_to_pdf(self, input_file: str, output_dir: str) -> Tuple[bool, str]:
        """
        Convert a file to PDF using LibreOffice
        
        Args:
            input_file: Path to input file
            output_dir: Directory to save the PDF
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.is_available():
            return False, "LibreOffice not found on system"
        
        if not os.path.exists(input_file):
            return False, f"Input file not found: {input_file}"
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Build LibreOffice command
            cmd = [
                self.libreoffice_path,
                '--headless',
                '--invisible',
                '--convert-to', 'pdf',
                '--outdir', output_dir,
                input_file
            ]
            
            # Run the conversion
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )
            
            if result.returncode == 0:
                # Check if PDF was created
                input_name = Path(input_file).stem
                output_pdf = os.path.join(output_dir, f"{input_name}.pdf")
                
                if os.path.exists(output_pdf):
                    return True, output_pdf
                else:
                    return False, "PDF conversion completed but output file not found"
            else:
                return False, f"LibreOffice conversion failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Conversion timed out after 60 seconds"
        except Exception as e:
            return False, f"Conversion error: {str(e)}"
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file extensions"""
        return [
            '.doc', '.docx',      # Word documents
            '.xls', '.xlsx',      # Excel spreadsheets  
            '.ppt', '.pptx',      # PowerPoint presentations
            '.odt', '.ods', '.odp'  # OpenDocument formats
        ]