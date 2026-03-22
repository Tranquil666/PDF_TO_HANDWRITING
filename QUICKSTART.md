# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/Tranquil666/PDF_TO_HANDWRITING.git
cd PDF_TO_HANDWRITING

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Create a Sample PDF (Optional)
```bash
python create_sample_pdf.py
```

### 2. Convert PDF to Handwriting
```bash
python pdf_to_handwriting.py sample.pdf
```

Your handwriting images will be saved in the `output/` directory!

## Common Use Cases

### Use Case 1: Basic Conversion
```bash
python pdf_to_handwriting.py mydocument.pdf
```

### Use Case 2: Custom Output Location
```bash
python pdf_to_handwriting.py mydocument.pdf -o my_handwriting
```

### Use Case 3: Larger Font
```bash
python pdf_to_handwriting.py mydocument.pdf --font-size 32 --line-spacing 45
```

### Use Case 4: Blue Ink Color
```bash
python pdf_to_handwriting.py mydocument.pdf --color "0,0,255"
```

### Use Case 5: Custom Everything
```bash
python pdf_to_handwriting.py mydocument.pdf \
    -o beautiful_handwriting \
    -p my_notes \
    --font-size 30 \
    --line-spacing 42 \
    --color "25,25,112" \
    --margin 180
```

## Python API Usage

```python
from pdf_to_handwriting import PDFToHandwriting

# Create converter
converter = PDFToHandwriting(
    font_size=30,
    line_spacing=45,
    text_color=(0, 0, 139)
)

# Convert PDF
images = converter.convert('input.pdf', output_dir='output')
print(f"Created {len(images)} handwriting images!")
```

## Tips for Best Results

1. **Use a handwriting font** for more realistic results
   - Download a free handwriting TTF font
   - Use: `--font /path/to/handwriting.ttf`

2. **Adjust font size** based on your needs
   - Smaller (24-26): More text per page
   - Medium (28-30): Good balance
   - Larger (32-36): Easier to read

3. **Match line spacing to font size**
   - Generally: line_spacing = font_size + 12-15 pixels

4. **Use blue ink** for authentic look
   - Dark blue: `--color "0,0,139"`
   - Navy blue: `--color "25,25,112"`
   - Royal blue: `--color "0,0,255"`

## Troubleshooting

**Problem: "No text found in PDF"**
- Your PDF might be scanned images
- Solution: Use OCR software first to convert to text-based PDF

**Problem: Font doesn't look like handwriting**
- Default system font is being used
- Solution: Download and specify a handwriting TTF font

**Problem: Text is cut off**
- Margins might be too large or font too big
- Solution: Reduce margins or font size

## Need Help?

Run this for all available options:
```bash
python pdf_to_handwriting.py --help
```

For more details, see the main [README.md](README.md)
