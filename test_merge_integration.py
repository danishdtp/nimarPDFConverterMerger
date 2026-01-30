#!/usr/bin/env python3
"""
Test the merge functionality by simulating GUI behavior
"""

import sys
import os
from pathlib import Path
import tempfile

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_merge_integration():
    """Test the full merge integration"""
    print("🧪 Testing Merge Integration")
    print("=" * 50)
    
    try:
        from conversion.converter import DocumentConverter
        from pdf_ops.merger import PDFMerger
        converter = DocumentConverter()
        merger = PDFMerger()
        print("✅ Successfully imported modules")
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test text files
            input_files = []
            for i in range(3):  # Create 3 files
                text_file = temp_path / f"document{i+1}.txt"
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(f"Document {i+1}\n")
                    f.write("This is test content for PDF conversion.\n")
                    f.write(f"Page {i+1} content.\n")
                    f.write("End of document.\n")
                input_files.append(str(text_file))
            
            print(f"✅ Created {len(input_files)} test documents")
            
            # Convert all to PDFs
            pdf_files = []
            for file_path in input_files:
                success, message = converter.convert_to_pdf(file_path, temp_dir)
                if success:
                    # The converter returns the path to the created PDF
                    pdf_path = Path(file_path).with_suffix('.pdf')
                    # Check if it has the _converted suffix pattern
                    if not pdf_path.exists():
                        pdf_path = Path(file_path).stem + "_converted.pdf"
                        pdf_path = temp_path / pdf_path
                    
                    if pdf_path.exists():
                        pdf_files.append(str(pdf_path))
                        print(f"✅ PDF created: {pdf_path.name}")
                    else:
                        print(f"❌ PDF not found for: {file_path}")
                else:
                    print(f"❌ Conversion failed: {message}")
            
            if len(pdf_files) >= 2:
                # Test merge
                print(f"\n🔗 Merging {len(pdf_files)} PDFs...")
                output_path = temp_path / "merged_result.pdf"
                success, message = merger.merge_pdfs(pdf_files, str(output_path))
                
                print(f"Merge result: {success}")
                print(f"Message: {message}")
                
                if success and output_path.exists():
                    file_size = output_path.stat().st_size
                    print(f"✅ Merged PDF: {output_path.name} ({file_size} bytes)")
                    
                    # Get PDF info
                    pdf_info = merger.get_pdf_info(str(output_path))
                    print(f"📊 PDF Info: {pdf_info}")
                    
                    # Verify it has all pages
                    expected_pages = len(pdf_files)
                    actual_pages = pdf_info.get('pages', 0)
                    if actual_pages >= expected_pages:
                        print(f"✅ Page count verification passed: {actual_pages} pages")
                        return True
                    else:
                        print(f"❌ Page count verification failed: {actual_pages} pages (expected {expected_pages})")
                        return False
                else:
                    print("❌ Merge failed - no output file")
                    return False
            else:
                print(f"❌ Not enough PDFs created: {len(pdf_files)}")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success = test_merge_integration()
    print(f"\n{'✅ MERGE INTEGRATION TEST PASSED' if success else '❌ MERGE INTEGRATION TEST FAILED'}")
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)