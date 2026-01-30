"""
PDF merging functionality using PyPDF2
"""

import os
from pathlib import Path
from typing import List, Tuple

from PyPDF2 import PdfMerger, PdfReader

class PDFMerger:
    """Handles merging multiple PDF files into a single PDF"""
    
    def __init__(self):
        pass
    
    def merge_pdfs(self, pdf_files: List[str], output_path: str) -> Tuple[bool, str]:
        """
        Merge multiple PDF files into a single PDF
        
        Args:
            pdf_files: List of PDF file paths to merge
            output_path: Path for merged output file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not pdf_files:
            return False, "No PDF files provided for merging"
        
        # Validate all input files
        for pdf_file in pdf_files:
            if not os.path.exists(pdf_file):
                return False, f"File not found: {pdf_file}"
            
            if not pdf_file.lower().endswith('.pdf'):
                return False, f"File is not a PDF: {pdf_file}"
        
        try:
            merger = PdfMerger()
            
            # Add each PDF to merger
            for pdf_file in pdf_files:
                try:
                    merger.append(pdf_file)
                except Exception as e:
                    return False, f"Error adding {pdf_file} to merger: {str(e)}"
            
            # Write the merged PDF
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            
            merger.close()
            
            # Verify output file was created
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return True, f"Successfully merged {len(pdf_files)} PDFs into {output_path}"
            else:
                return False, "Merge completed but output file is empty or missing"
                
        except Exception as e:
            return False, f"PDF merge failed: {str(e)}"
    
    def get_pdf_info(self, pdf_file: str) -> dict:
        """Get information about a PDF file"""
        try:
            with open(pdf_file, 'rb') as file:
                reader = PdfReader(file)
                
                metadata = reader.metadata or {}
                
                return {
                    'pages': len(reader.pages),
                    'title': metadata.get('/Title', 'Unknown'),
                    'author': metadata.get('/Author', 'Unknown'),
                    'creator': metadata.get('/Creator', 'Unknown'),
                    'size': os.path.getsize(pdf_file)
                }
        except Exception as e:
            return {
                'error': str(e),
                'pages': 0,
                'title': 'Error reading PDF',
                'author': '',
                'creator': '',
                'size': 0
            }
    
    def can_merge(self, pdf_files: List[str]) -> Tuple[bool, str]:
        """Check if files can be merged"""
        if not pdf_files:
            return False, "No files provided"
        
        if len(pdf_files) < 2:
            return False, "At least 2 PDF files are required for merging"
        
        # Check if all files are PDFs and exist
        for pdf_file in pdf_files:
            if not os.path.exists(pdf_file):
                return False, f"File not found: {pdf_file}"
            
            if not pdf_file.lower().endswith('.pdf'):
                return False, f"File is not a PDF: {pdf_file}"
            
            # Try to read each PDF
            try:
                with open(pdf_file, 'rb') as file:
                    reader = PdfReader(file)
                    # This will raise an exception if PDF is corrupted
                    _ = len(reader.pages)
            except Exception as e:
                return False, f"Cannot read PDF file {pdf_file}: {str(e)}"
        
        return True, f"Can merge {len(pdf_files)} PDF files"
    
    def estimate_merged_size(self, pdf_files: List[str]) -> int:
        """Estimate size of merged PDF"""
        total_size = 0
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                total_size += os.path.getsize(pdf_file)
        
        # Add some overhead for merging (usually small)
        return int(total_size * 1.05)
    
    def get_total_pages(self, pdf_files: List[str]) -> int:
        """Get total number of pages across all PDF files"""
        total_pages = 0
        for pdf_file in pdf_files:
            try:
                with open(pdf_file, 'rb') as file:
                    reader = PdfReader(file)
                    total_pages += len(reader.pages)
            except:
                continue
        
        return total_pages