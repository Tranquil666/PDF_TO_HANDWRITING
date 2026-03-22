# Web Interface - Live Testing Guide

## Running the Live Web Server

The PDF to Handwriting Converter now includes a live web interface for easy testing and usage through your browser.

### Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the web server:**
```bash
python app.py
```

3. **Open your browser:**
Navigate to `http://127.0.0.1:5000` or `http://localhost:5000`

### Using the Web Interface

The web interface provides an intuitive drag-and-drop experience:

1. **Upload PDF**: Click "Choose PDF File" and select your PDF document
2. **Configure Settings** (optional):
   - **Font Size**: Adjust between 12-50 pixels (default: 28)
   - **Line Spacing**: Set between 20-80 pixels (default: 40)
   - **Margin**: Choose between 50-400 pixels (default: 200)
   - **Text Color**: RGB format like `0,0,139` (default: dark blue)
   - **Background Color**: RGBA format like `255,255,255,255` (default: white)
3. **Convert**: Click "Convert to Handwriting" button
4. **Download**: Your converted image(s) will download automatically
   - Single page PDFs → Download as PNG image
   - Multi-page PDFs → Download as ZIP file containing all pages

### Server Information

- **Port**: 5000 (default)
- **Host**: 0.0.0.0 (accessible from network)
- **Max File Size**: 16MB
- **Supported Formats**: PDF files only (text-based)

### API Endpoints

#### GET `/`
Main web interface page

#### POST `/convert`
Convert PDF to handwriting images

**Form Parameters:**
- `pdf_file` (file, required): PDF file to convert
- `font_size` (int, optional): Font size in pixels (default: 28)
- `line_spacing` (int, optional): Line spacing in pixels (default: 40)
- `margin` (int, optional): Margin in pixels (default: 200)
- `color` (string, optional): Text color as "R,G,B" (default: "0,0,139")
- `bg_color` (string, optional): Background color as "R,G,B,A" (default: "255,255,255,255")

**Example using cURL:**
```bash
curl -F "pdf_file=@document.pdf" \
     -F "font_size=30" \
     -F "line_spacing=45" \
     -F "color=0,0,139" \
     http://localhost:5000/convert \
     -o output.png
```

#### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "service": "PDF to Handwriting Converter"
}
```

### Features

✅ **Beautiful UI**: Modern, responsive design with gradient backgrounds
✅ **Drag & Drop**: Easy file upload experience
✅ **Real-time Preview**: See your settings before conversion
✅ **Automatic Download**: Single images or ZIP files for multi-page PDFs
✅ **Form Validation**: Client-side validation for all inputs
✅ **Error Handling**: Clear error messages for troubleshooting
✅ **Mobile Friendly**: Responsive design works on all devices

### Configuration Tips

**For Realistic Handwriting:**
- Font Size: 28-32 pixels
- Line Spacing: 40-50 pixels
- Text Color: `0,0,139` (dark blue ink)
- Background: `255,255,255,255` (white paper)

**For Dense Text:**
- Font Size: 24 pixels
- Line Spacing: 35 pixels
- Margin: 150 pixels

**For Presentation:**
- Font Size: 32 pixels
- Line Spacing: 55 pixels
- Margin: 250 pixels

### File Structure

```
PDF_TO_HANDWRITING/
├── app.py                    # Flask web application
├── templates/
│   └── index.html           # Web interface template
├── uploads/                 # Temporary upload directory (auto-created)
├── web_output/              # Conversion output directory (auto-created)
└── pdf_to_handwriting.py    # Core conversion module
```

### Production Deployment

⚠️ **Warning**: The included server uses Flask's development server. For production use, deploy with a WSGI server like:

**Using Gunicorn:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Using uWSGI:**
```bash
pip install uwsgi
uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app --processes 4
```

### Troubleshooting

**Server won't start:**
- Check if port 5000 is already in use
- Try running on different port: `python app.py` (edit app.py to change port)

**Upload fails:**
- Check file size (max 16MB)
- Ensure file is a valid PDF
- Verify the PDF contains actual text (not scanned images)

**Conversion errors:**
- Check Flask logs in terminal
- Ensure all dependencies are installed
- Verify PDF is text-based, not image-based

**Can't access from network:**
- Check firewall settings
- Server runs on 0.0.0.0 by default (all interfaces)
- Access via `http://YOUR_IP:5000`

### Security Notes

For production deployment:
1. Change the secret key in `app.py`
2. Use HTTPS/TLS encryption
3. Implement authentication if needed
4. Add rate limiting
5. Scan uploads for malware
6. Use a production WSGI server

### Development Mode

The server runs in debug mode by default, which:
- Auto-reloads on code changes
- Shows detailed error pages
- Provides debugging tools
- Should NOT be used in production

To disable debug mode, edit `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

### Support

For issues or questions:
- Check the logs in your terminal
- Review this documentation
- Open an issue on GitHub
- Ensure all dependencies are correctly installed

### Next Steps

- Try converting different PDF files
- Experiment with settings to find your preferred style
- Use the API endpoint for automation
- Integrate into your own applications
