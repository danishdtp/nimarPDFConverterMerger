#!/usr/bin/env python3
"""
Test merge functionality directly using the converter
"""

import sys
import os
from pathlib import Path
import tempfile

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_basic_merge():
    """Test basic merge functionality"""
    print("🧪 Testing PDF Merge Functionality")
    print("=" * 50)
    
    try:
        from conversion.converter import DocumentConverter
        converter = DocumentConverter()
        print("✅ Successfully imported converter")
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test text files
            test_files = []
            for i in range(2):
                text_file = temp_path / f"test{i+1}.txt"
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(f"This is test document {i+1}\n")
                    f.write(f"Content for document {i+1}\n")
                    f.write("Some sample text content.\n")
                
                # Convert to PDF
                success, message = converter.convert_to_pdf(str(text_file), temp_dir)
                print(f"Conversion result: {success} - {message}")
                pdf_file = temp_path / f"test{i+1}.pdf"
                print(f"Looking for PDF file: {pdf_file}")
                # Check both possible names
                pdf_name = f"test{i+1}_converted.pdf"
                converted_file = temp_path / pdf_name
                if converted_file.exists():
                    test_files.append(str(converted_file))
                    print(f"✅ Created PDF: {converted_file.name}")
                elif pdf_file.exists():
                    test_files.append(str(pdf_file))
                    print(f"✅ Created PDF: {pdf_file.name}")
                else:
                    print(f"❌ PDF not found: {pdf_file.name} or {converted_file.name}")
            
            if len(test_files) >= 2:
                # Test merge functionality
                print(f"\n🔗 Testing merge with {len(test_files)} PDFs...")
                
                from pdf_ops.merger import PDFMerger
                merger = PDFMerger()
                
                output_file = temp_path / "merged.pdf"
                success, message = merger.merge_pdfs(test_files, str(output_file))
                print(f"Merge result: {success} - {message}")
                
                if success and output_file.exists():
                    file_size = output_file.stat().st_size
                    print(f"✅ Merged PDF created: {output_file.name} ({file_size} bytes)")
                    
                    # Get PDF info
                    pdf_info = merger.get_pdf_info(str(output_file))
                    print(f"📊 PDF Info: {pdf_info}")
                    return True
                else:
                    print("❌ Merge failed")
                    return False
            else:
                print("❌ Not enough PDFs created for merge test")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success = test_basic_merge()
    print(f"\n{'✅ PASS' if success else '❌ FAIL'}")
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)