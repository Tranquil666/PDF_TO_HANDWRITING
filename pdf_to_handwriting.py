#!/usr/bin/env python3
"""
PDF to Handwriting Converter
Converts PDF text to handwriting-style images with realistic appearance.
"""

import os
import sys
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import PyPDF2
import random
import textwrap


class PDFToHandwriting:
    """Main class for converting PDF to handwriting-style images."""

    def __init__(self,
                 font_path: Optional[str] = None,
                 font_size: int = 28,
                 line_spacing: int = 40,
                 page_width: int = 2480,
                 page_height: int = 3508,
                 margin_left: int = 200,
                 margin_right: int = 200,
                 margin_top: int = 200,
                 margin_bottom: int = 200,
                 text_color: Tuple[int, int, int] = (0, 0, 139),
                 background_color: Tuple[int, int, int, int] = (255, 255, 255, 255)):
        """
        Initialize the PDF to Handwriting converter.

        Args:
            font_path: Path to TTF font file. If None, uses default system font
            font_size: Size of the font
            line_spacing: Spacing between lines in pixels
            page_width: Width of output image in pixels (A4 at 300 DPI = 2480)
            page_height: Height of output image in pixels (A4 at 300 DPI = 3508)
            margin_left: Left margin in pixels
            margin_right: Right margin in pixels
            margin_top: Top margin in pixels
            margin_bottom: Bottom margin in pixels
            text_color: RGB color tuple for text
            background_color: RGBA color tuple for background
        """
        self.font_size = font_size
        self.line_spacing = line_spacing
        self.page_width = page_width
        self.page_height = page_height
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.text_color = text_color
        self.background_color = background_color

        # Calculate usable writing area
        self.text_width = page_width - margin_left - margin_right
        self.text_height = page_height - margin_top - margin_bottom

        # Load font
        try:
            if font_path and os.path.exists(font_path):
                self.font = ImageFont.truetype(font_path, font_size)
            else:
                # Try to use a default handwriting-like font
                # Fall back to DejaVuSans if no handwriting font is available
                try:
                    self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                except:
                    # If all else fails, use default font
                    self.font = ImageFont.load_default()
                    print("Warning: Using default font. For better handwriting effect, provide a handwriting font.")
        except Exception as e:
            print(f"Warning: Could not load font: {e}. Using default font.")
            self.font = ImageFont.load_default()

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text as a string

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF cannot be read
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                    text += "\n\n"  # Add spacing between pages

                return text.strip()
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")

    def wrap_text(self, text: str, max_chars_per_line: int) -> List[str]:
        """
        Wrap text to fit within specified width.

        Args:
            text: Text to wrap
            max_chars_per_line: Maximum characters per line

        Returns:
            List of wrapped lines
        """
        lines = []
        paragraphs = text.split('\n')

        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append("")  # Preserve empty lines
                continue

            wrapped = textwrap.wrap(paragraph, width=max_chars_per_line,
                                   break_long_words=False,
                                   replace_whitespace=False)
            if wrapped:
                lines.extend(wrapped)
            else:
                lines.append("")

        return lines

    def add_handwriting_variation(self, x: int, y: int) -> Tuple[int, int]:
        """
        Add slight random variations to position for more natural handwriting look.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Modified (x, y) coordinates
        """
        # Add small random variations
        x_variation = random.randint(-2, 2)
        y_variation = random.randint(-1, 1)
        return (x + x_variation, y + y_variation)

    def create_handwriting_image(self, text: str) -> List[Image.Image]:
        """
        Convert text to handwriting-style images.

        Args:
            text: Text to convert

        Returns:
            List of PIL Image objects
        """
        # Estimate characters per line based on font size
        avg_char_width = self.font_size * 0.6
        max_chars_per_line = int(self.text_width / avg_char_width)

        # Wrap text
        lines = self.wrap_text(text, max_chars_per_line)

        # Calculate lines per page
        lines_per_page = int(self.text_height / self.line_spacing)

        # Split lines into pages
        pages = []
        current_page_lines = []

        for line in lines:
            current_page_lines.append(line)
            if len(current_page_lines) >= lines_per_page:
                pages.append(current_page_lines)
                current_page_lines = []

        # Add remaining lines as last page
        if current_page_lines:
            pages.append(current_page_lines)

        # Create images for each page
        images = []
        for page_lines in pages:
            # Create new image
            img = Image.new('RGBA', (self.page_width, self.page_height), self.background_color)
            draw = ImageDraw.Draw(img)

            # Draw text line by line
            y_position = self.margin_top

            for line in page_lines:
                if line.strip():  # Only draw non-empty lines
                    # Add slight variation for handwriting effect
                    x_pos, y_pos = self.add_handwriting_variation(self.margin_left, y_position)
                    draw.text((x_pos, y_pos), line, font=self.font, fill=self.text_color)

                y_position += self.line_spacing

            images.append(img)

        return images

    def convert(self, pdf_path: str, output_dir: str = "output",
                output_prefix: str = "handwriting") -> List[str]:
        """
        Convert PDF to handwriting images.

        Args:
            pdf_path: Path to input PDF file
            output_dir: Directory to save output images
            output_prefix: Prefix for output image filenames

        Returns:
            List of paths to generated images

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF cannot be processed
        """
        # Extract text from PDF
        print(f"Extracting text from {pdf_path}...")
        text = self.extract_text_from_pdf(pdf_path)

        if not text.strip():
            raise ValueError("No text found in PDF. The PDF might be image-based or empty.")

        print(f"Extracted {len(text)} characters")

        # Create handwriting images
        print("Creating handwriting images...")
        images = self.create_handwriting_image(text)

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Save images
        output_paths = []
        for i, img in enumerate(images, 1):
            output_path = os.path.join(output_dir, f"{output_prefix}_page_{i}.png")
            img.save(output_path, 'PNG', dpi=(300, 300))
            output_paths.append(output_path)
            print(f"Saved: {output_path}")

        return output_paths


def main():
    """Command-line interface for PDF to Handwriting converter."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert PDF to handwriting-style images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf
  %(prog)s input.pdf -o my_output -p handwritten
  %(prog)s input.pdf --font /path/to/handwriting.ttf --font-size 30
  %(prog)s input.pdf --color "0,0,255" --bg "255,255,200,255"
        """
    )

    parser.add_argument('pdf_path', help='Path to input PDF file')
    parser.add_argument('-o', '--output-dir', default='output',
                       help='Output directory (default: output)')
    parser.add_argument('-p', '--prefix', default='handwriting',
                       help='Output filename prefix (default: handwriting)')
    parser.add_argument('--font', help='Path to TTF font file for handwriting style')
    parser.add_argument('--font-size', type=int, default=28,
                       help='Font size (default: 28)')
    parser.add_argument('--line-spacing', type=int, default=40,
                       help='Line spacing in pixels (default: 40)')
    parser.add_argument('--color', default='0,0,139',
                       help='Text color as R,G,B (default: 0,0,139 - dark blue)')
    parser.add_argument('--bg', default='255,255,255,255',
                       help='Background color as R,G,B,A (default: 255,255,255,255 - white)')
    parser.add_argument('--margin', type=int, default=200,
                       help='Margin size in pixels for all sides (default: 200)')

    args = parser.parse_args()

    # Parse colors
    try:
        text_color = tuple(map(int, args.color.split(',')))
        if len(text_color) != 3:
            raise ValueError("Text color must have 3 values (R,G,B)")
    except Exception as e:
        print(f"Error: Invalid text color format: {e}")
        sys.exit(1)

    try:
        bg_color = tuple(map(int, args.bg.split(',')))
        if len(bg_color) != 4:
            raise ValueError("Background color must have 4 values (R,G,B,A)")
    except Exception as e:
        print(f"Error: Invalid background color format: {e}")
        sys.exit(1)

    try:
        # Create converter
        converter = PDFToHandwriting(
            font_path=args.font,
            font_size=args.font_size,
            line_spacing=args.line_spacing,
            margin_left=args.margin,
            margin_right=args.margin,
            margin_top=args.margin,
            margin_bottom=args.margin,
            text_color=text_color,
            background_color=bg_color
        )

        # Convert PDF
        output_paths = converter.convert(args.pdf_path, args.output_dir, args.prefix)

        print(f"\n✓ Successfully created {len(output_paths)} handwriting image(s)")
        print(f"✓ Output saved to: {args.output_dir}/")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
