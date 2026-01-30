"""
Python library-based document conversion
"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

class PythonConverter:
    """Handles document conversion using Python libraries"""
    
    def __init__(self):
        self.supported_formats = self._get_supported_formats()
        
    def _get_supported_formats(self) -> List[str]:
        """Determine supported formats based on available libraries"""
        formats = ['.txt', '.csv']  # Basic text formats always supported
        
        try:
            import markdown
            formats.append('.md')
        except ImportError:
            pass
            
        try:
            import pdfkit
            formats.extend(['.html', '.htm'])
        except ImportError:
            pass
            
        try:
            import pypandoc
            # Pandoc supports many formats but we'll list the main ones
            formats.extend(['.xml', '.rst', '.tex'])
        except ImportError:
            pass
        
        # Add image formats (always supported with Pillow)
        try:
            from PIL import Image
            formats.extend([
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
                '.tiff', '.tif', '.webp', '.ico'
            ])
        except ImportError:
            pass
            
        return formats
    
    def convert_to_pdf(self, input_file: str, output_dir: str) -> Tuple[bool, str]:
        """
        Convert a file to PDF using appropriate Python library
        
        Args:
            input_file: Path to input file
            output_dir: Directory to save PDF
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        input_path = Path(input_file)
        ext = input_path.suffix.lower()
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        output_pdf = os.path.join(output_dir, f"{input_path.stem}_converted.pdf")
        
        try:
            if ext == '.txt':
                return self._convert_txt_to_pdf(input_file, output_pdf)
            elif ext == '.csv':
                return self._convert_csv_to_pdf(input_file, output_pdf)
            elif ext == '.md':
                return self._convert_markdown_to_pdf(input_file, output_pdf)
            elif ext in ['.html', '.htm']:
                return self._convert_html_to_pdf(input_file, output_pdf)
            elif ext == '.xml':
                return self._convert_xml_to_pdf(input_file, output_pdf)
            elif ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico']:
                return self._convert_image_to_pdf(input_file, output_pdf)
            else:
                return False, f"Unsupported format: {ext}"
                
        except Exception as e:
            return False, f"Conversion error: {str(e)}"
    
    def _convert_txt_to_pdf(self, input_file: str, output_file: str) -> Tuple[bool, str]:
        """Convert text file to PDF"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import inch
            
            c = canvas.Canvas(output_file, pagesize=A4)
            width, height = A4
            
            # Set up margins
            margin = inch
            y_position = height - margin
            line_height = 14
            
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Split into lines and draw
                for line in content.split('\n'):
                    if y_position < margin:  # New page if needed
                        c.showPage()
                        y_position = height - margin
                    
                    c.drawString(margin, y_position, line)
                    y_position -= line_height
            
            c.save()
            return True, output_file
            
        except ImportError:
            return False, "ReportLab library not available for text conversion"
        except Exception as e:
            return False, f"Text conversion failed: {str(e)}"
    
    def _convert_csv_to_pdf(self, input_file: str, output_file: str) -> Tuple[bool, str]:
        """Convert CSV to PDF"""
        try:
            import csv
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import inch
            
            c = canvas.Canvas(output_file, pagesize=A4)
            width, height = A4
            
            # Set up margins
            margin = inch
            y_position = height - margin
            line_height = 14
            
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if y_position < margin:  # New page if needed
                        c.showPage()
                        y_position = height - margin
                    
                    # Convert row to string and draw
                    text = ' | '.join(str(cell) for cell in row)
                    c.drawString(margin, y_position, text)
                    y_position -= line_height
            
            c.save()
            return True, output_file
            
        except ImportError:
            return False, "Required libraries not available for CSV conversion"
        except Exception as e:
            return False, f"CSV conversion failed: {str(e)}"
    
    def _convert_markdown_to_pdf(self, input_file: str, output_file: str) -> Tuple[bool, str]:
        """Convert Markdown to PDF"""
        try:
            import markdown
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph
            
            # Read markdown file
            with open(input_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Convert to HTML
            html = markdown.markdown(md_content)
            
            # Create PDF
            doc = SimpleDocTemplate(output_file, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Convert HTML to paragraphs
            for line in html.split('\n'):
                if line.strip():
                    para = Paragraph(line, styles['Normal'])
                    story.append(para)
            
            doc.build(story)
            return True, output_file
            
        except ImportError:
            return False, "Markdown library not available for conversion"
        except Exception as e:
            return False, f"Markdown conversion failed: {str(e)}"
    
    def _convert_html_to_pdf(self, input_file: str, output_file: str) -> Tuple[bool, str]:
        """Convert HTML to PDF"""
        try:
            import pdfkit
            
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': 'UTF-8',
                'no-outline': None
            }
            
            pdfkit.from_file(input_file, output_file, options=options)
            return True, output_file
            
        except ImportError:
            return False, "pdfkit library not available for HTML conversion"
        except Exception as e:
            return False, f"HTML conversion failed: {str(e)}"
    
    def _convert_xml_to_pdf(self, input_file: str, output_file: str) -> Tuple[bool, str]:
        """Convert XML to PDF (basic implementation)"""
        try:
            import xml.etree.ElementTree as ET
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            
            tree = ET.parse(input_file)
            root = tree.getroot()
            
            c = canvas.Canvas(output_file, pagesize=A4)
            width, height = A4
            
            # Simple text extraction and rendering
            y_position = height - 50
            text = self._extract_text_from_xml(root)
            
            for line in text.split('\n'):
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50
                
                c.drawString(50, y_position, line)
                y_position -= 15
            
            c.save()
            return True, output_file
            
        except Exception as e:
            return False, f"XML conversion failed: {str(e)}"
    
    def _convert_image_to_pdf(self, input_file: str, output_file: str) -> Tuple[bool, str]:
        """Convert image to PDF"""
        try:
            from PIL import Image
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            
            # Open and validate image
            with Image.open(input_file) as img:
                # Convert RGBA to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Calculate dimensions to fit page
                img_width, img_height = img.size
                page_width, page_height = A4  # Use A4 for better image compatibility
                margin = 50  # 50pt margins
                
                # Calculate scaling to fit page while maintaining aspect ratio
                max_width = page_width - 2 * margin
                max_height = page_height - 2 * margin
                
                scale_w = max_width / img_width
                scale_h = max_height / img_height
                scale = min(scale_w, scale_h)
                
                # Scale image dimensions
                scaled_width = img_width * scale
                scaled_height = img_height * scale
                
                # Calculate center position
                x_pos = (page_width - scaled_width) / 2
                y_pos = (page_height - scaled_height) / 2
                
                # Create PDF
                c = canvas.Canvas(output_file, pagesize=A4)
                
                # Draw image centered on page
                c.drawImage(
                    input_file,
                    x_pos, y_pos,
                    width=scaled_width,
                    height=scaled_height,
                    preserveAspectRatio=True
                )
                
                # Add filename as caption
                filename = Path(input_file).stem
                c.setFont("Helvetica", 10)
                c.setFillColorRGB(0.5, 0.5, 0.5)  # Gray color
                c.drawString(margin, margin - 20, f"Image: {filename}")
                
                c.save()
            
            return True, output_file
            
        except ImportError:
            return False, "PIL (Pillow) and ReportLab libraries required for image conversion"
        except Exception as e:
            return False, f"Image conversion failed: {str(e)}"
    
    def _extract_text_from_xml(self, element) -> str:
        """Extract text content from XML element"""
        text = element.text or ""
        for child in element:
            text += self._extract_text_from_xml(child)
        text += element.tail or ""
        return text
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file extensions"""
        return self.supported_formats