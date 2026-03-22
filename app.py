#!/usr/bin/env python3
"""
Flask Web Application for PDF to Handwriting Converter
Provides a live web interface for testing the PDF to handwriting conversion tool
"""

import os
import zipfile
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pdf_to_handwriting import PDFToHandwriting

app = Flask(__name__)
app.secret_key = 'pdf-to-handwriting-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'web_output'

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main upload page"""
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """Handle PDF upload and conversion"""
    # Check if file was uploaded
    if 'pdf_file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))

    file = request.files['pdf_file']

    # Check if filename is empty
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    # Check if file is allowed
    if not allowed_file(file.filename):
        flash('Only PDF files are allowed', 'error')
        return redirect(url_for('index'))

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Get conversion parameters from form
        font_size = int(request.form.get('font_size', 28))
        line_spacing = int(request.form.get('line_spacing', 40))
        margin = int(request.form.get('margin', 200))

        # Parse color (R,G,B format)
        color_str = request.form.get('color', '0,0,139')
        text_color = tuple(map(int, color_str.split(',')))

        # Parse background color (R,G,B,A format)
        bg_str = request.form.get('bg_color', '255,255,255,255')
        bg_color = tuple(map(int, bg_str.split(',')))

        # Create converter instance
        converter = PDFToHandwriting(
            font_size=font_size,
            line_spacing=line_spacing,
            text_color=text_color,
            background_color=bg_color,
            margin=margin
        )

        # Convert PDF to handwriting images
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], filename.rsplit('.', 1)[0])
        os.makedirs(output_dir, exist_ok=True)

        output_paths = converter.convert(upload_path, output_dir=output_dir)

        # Clean up uploaded file
        os.remove(upload_path)

        # If only one image, send it directly
        if len(output_paths) == 1:
            return send_file(
                output_paths[0],
                as_attachment=True,
                download_name=f"{filename.rsplit('.', 1)[0]}_handwriting.png"
            )

        # If multiple images, create a zip file
        zip_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{filename.rsplit('.', 1)[0]}_handwriting.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for i, img_path in enumerate(output_paths):
                zipf.write(img_path, os.path.basename(img_path))

        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"{filename.rsplit('.', 1)[0]}_handwriting.zip"
        )

    except Exception as e:
        flash(f'Error converting PDF: {str(e)}', 'error')
        # Clean up if error occurs
        if os.path.exists(upload_path):
            os.remove(upload_path)
        return redirect(url_for('index'))

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'service': 'PDF to Handwriting Converter'}

if __name__ == '__main__':
    print("\n" + "="*60)
    print("PDF to Handwriting Converter - Live Web Interface")
    print("="*60)
    print("\n🌐 Server starting at: http://127.0.0.1:5000")
    print("📝 Upload PDFs and convert them to handwriting-style images")
    print("\nPress Ctrl+C to stop the server\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
