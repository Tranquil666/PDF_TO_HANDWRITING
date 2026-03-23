"""
PDF Conversion endpoint for Vercel deployment
Handles PDF upload and conversion to handwriting-style images
"""
from http.server import BaseHTTPRequestHandler
import sys
import os
import json
import tempfile
import zipfile
import base64
from io import BytesIO
import cgi

# Add parent directory to path to import pdf_to_handwriting module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pdf_to_handwriting import PDFToHandwriting
except ImportError:
    # If import fails, we'll handle it in the function
    PDFToHandwriting = None


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle PDF upload and conversion"""
        try:
            # Check if PDFToHandwriting module is available
            if PDFToHandwriting is None:
                self.send_error(500, "PDF conversion module not available")
                return

            # Parse the multipart form data
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Content-Type must be multipart/form-data")
                return

            # Parse form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )

            # Get the uploaded PDF file
            if 'pdf_file' not in form:
                self.send_error(400, "No PDF file uploaded")
                return

            pdf_file = form['pdf_file']
            if not pdf_file.file:
                self.send_error(400, "No file data")
                return

            # Get conversion parameters
            try:
                font_size = int(form.getvalue('font_size', '28'))
                line_spacing = int(form.getvalue('line_spacing', '40'))
                margin = int(form.getvalue('margin', '200'))

                # Parse color (R,G,B format)
                color_str = form.getvalue('color', '0,0,139')
                text_color = tuple(map(int, color_str.split(',')))

                # Parse background color (R,G,B,A format)
                bg_str = form.getvalue('bg_color', '255,255,255,255')
                bg_color = tuple(map(int, bg_str.split(',')))
            except (ValueError, TypeError) as e:
                self.send_error(400, f"Invalid parameters: {str(e)}")
                return

            # Create temporary directory for processing
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save uploaded PDF to temp file
                pdf_filename = pdf_file.filename or 'upload.pdf'
                pdf_path = os.path.join(temp_dir, 'input.pdf')

                with open(pdf_path, 'wb') as f:
                    f.write(pdf_file.file.read())

                # Create output directory
                output_dir = os.path.join(temp_dir, 'output')
                os.makedirs(output_dir, exist_ok=True)

                # Create converter instance and process
                converter = PDFToHandwriting(
                    font_size=font_size,
                    line_spacing=line_spacing,
                    text_color=text_color,
                    background_color=bg_color,
                    margin=margin
                )

                # Convert PDF
                output_paths = converter.convert(pdf_path, output_dir=output_dir)

                if not output_paths:
                    self.send_error(500, "Conversion failed - no output generated")
                    return

                # If only one image, send it directly
                if len(output_paths) == 1:
                    with open(output_paths[0], 'rb') as f:
                        image_data = f.read()

                    self.send_response(200)
                    self.send_header('Content-Type', 'image/png')
                    self.send_header('Content-Disposition',
                                   f'attachment; filename="{pdf_filename.rsplit(".", 1)[0]}_handwriting.png"')
                    self.send_header('Content-Length', str(len(image_data)))
                    self.end_headers()
                    self.wfile.write(image_data)
                else:
                    # Multiple images - create a ZIP file
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for img_path in output_paths:
                            zipf.write(img_path, os.path.basename(img_path))

                    zip_data = zip_buffer.getvalue()

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/zip')
                    self.send_header('Content-Disposition',
                                   f'attachment; filename="{pdf_filename.rsplit(".", 1)[0]}_handwriting.zip"')
                    self.send_header('Content-Length', str(len(zip_data)))
                    self.end_headers()
                    self.wfile.write(zip_data)

        except Exception as e:
            # Send error response
            error_msg = f"Error processing PDF: {str(e)}"
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': error_msg}).encode())

    def do_GET(self):
        """Handle GET requests - redirect to home"""
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
