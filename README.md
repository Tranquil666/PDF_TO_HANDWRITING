# PDF to Handwriting Converter

A Python tool that converts PDF documents to handwriting-style images. This tool extracts text from PDFs and renders it in a handwriting-like appearance, creating realistic-looking handwritten pages.

## Features

- ✅ Extracts text from PDF files accurately
- ✅ Converts text to handwriting-style images
- ✅ Customizable font, size, and spacing
- ✅ Adjustable margins and page dimensions
- ✅ Custom text and background colors
- ✅ Automatic text wrapping and pagination
- ✅ Multiple page output support
- ✅ High-quality 300 DPI output
- ✅ Command-line interface
- ✅ **Web interface for live testing** 🆕
- ✅ Error handling and validation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Tranquil666/PDF_TO_HANDWRITING.git
cd PDF_TO_HANDWRITING
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended for Testing)

Start the live web server for an easy-to-use browser interface:

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

Features:
- 🎨 Beautiful, intuitive interface
- 📤 Drag-and-drop file upload
- ⚙️ Real-time settings configuration
- 💾 Automatic download of converted images
- 📱 Mobile-friendly responsive design

For detailed web interface documentation, see [WEB_INTERFACE.md](WEB_INTERFACE.md)

### Command-Line Interface

#### Basic Usage

Convert a PDF to handwriting images:
```bash
python pdf_to_handwriting.py input.pdf
```

This will create handwriting-style images in the `output/` directory.

#### Advanced Options

```bash
python pdf_to_handwriting.py input.pdf \
    --output-dir my_output \
    --prefix handwritten \
    --font /path/to/handwriting.ttf \
    --font-size 30 \
    --line-spacing 45 \
    --color "0,0,255" \
    --bg "255,255,200,255" \
    --margin 250
```

#### Command-Line Arguments

- `pdf_path` - Path to input PDF file (required)
- `-o, --output-dir` - Output directory (default: `output`)
- `-p, --prefix` - Output filename prefix (default: `handwriting`)
- `--font` - Path to TTF font file for handwriting style
- `--font-size` - Font size in pixels (default: 28)
- `--line-spacing` - Line spacing in pixels (default: 40)
- `--color` - Text color as R,G,B (default: `0,0,139` - dark blue)
- `--bg` - Background color as R,G,B,A (default: `255,255,255,255` - white)
- `--margin` - Margin size in pixels for all sides (default: 200)

### Python API

You can also use the tool programmatically:

```python
from pdf_to_handwriting import PDFToHandwriting

# Create converter with custom settings
converter = PDFToHandwriting(
    font_size=30,
    line_spacing=45,
    text_color=(0, 0, 139),
    background_color=(255, 255, 255, 255)
)

# Convert PDF to handwriting images
output_paths = converter.convert('input.pdf', output_dir='output')

print(f"Created {len(output_paths)} images")
```

## Requirements

- Python 3.7+
- Pillow >= 10.0.0
- PyPDF2 >= 3.0.0
- reportlab >= 4.0.0
- fpdf2 >= 2.7.0

## How It Works

1. **PDF Text Extraction**: The tool uses PyPDF2 to extract text content from the PDF file
2. **Text Processing**: Text is wrapped and formatted to fit within page margins
3. **Image Generation**: Each page is rendered as a high-quality image using PIL/Pillow
4. **Handwriting Effect**: The tool applies slight random variations to character positions for a more natural handwriting appearance
5. **Output**: Images are saved as PNG files with 300 DPI resolution

## Output

The tool generates PNG images with the following characteristics:
- **Resolution**: 300 DPI (print quality)
- **Size**: A4 paper dimensions (2480 x 3508 pixels)
- **Format**: PNG with transparency support
- **Naming**: `{prefix}_page_{number}.png`

## Tips for Best Results

1. **Use Handwriting Fonts**: For the most realistic results, use a TTF handwriting font. You can find free handwriting fonts online.

2. **Adjust Font Size**: Experiment with font sizes between 24-32 for optimal readability.

3. **Fine-tune Spacing**: Adjust line spacing based on your font size to avoid overlapping text.

4. **Custom Colors**: Use blue ink color (0,0,139) for a more authentic handwriting look, or customize as needed.

5. **Margins**: Keep adequate margins (150-250 pixels) for a professional appearance.

## Error Handling

The tool includes comprehensive error handling for:
- Missing or invalid PDF files
- Empty or image-based PDFs (no extractable text)
- Font loading failures (falls back to default font)
- Invalid color formats
- Output directory creation

## Limitations

- Only works with text-based PDFs (not scanned images)
- Complex PDF formatting may not be preserved
- Tables and special layouts may not render perfectly
- For scanned PDFs, consider using OCR first

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Examples

### Example 1: Basic Conversion
```bash
python pdf_to_handwriting.py document.pdf
```
Output: `output/handwriting_page_1.png`, `output/handwriting_page_2.png`, etc.

### Example 2: Custom Output Location
```bash
python pdf_to_handwriting.py report.pdf -o converted -p myreport
```
Output: `converted/myreport_page_1.png`, etc.

### Example 3: With Custom Font
```bash
python pdf_to_handwriting.py notes.pdf --font HandwritingFont.ttf --font-size 32
```

### Example 4: Custom Colors
```bash
python pdf_to_handwriting.py letter.pdf --color "25,25,112" --bg "255,248,220,255"
```

## Troubleshooting

**No text extracted from PDF:**
- Ensure the PDF contains actual text and not just scanned images
- Try opening the PDF in a text editor to verify it contains text

**Font issues:**
- If the default font doesn't look good, download a handwriting TTF font
- Ensure the font file path is correct and accessible

**Output quality issues:**
- Increase font size and line spacing for better readability
- Adjust margins to ensure text fits properly on the page

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.
