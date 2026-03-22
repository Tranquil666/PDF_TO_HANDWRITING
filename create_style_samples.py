#!/usr/bin/env python3
"""
Demonstration script showing different output styles for PDF to Handwriting converter.
Creates sample outputs with various configurations.
"""

from pdf_to_handwriting import PDFToHandwriting
import os


def create_style_samples():
    """Create multiple output styles to demonstrate capabilities."""

    print("=" * 70)
    print("Creating PDF to Handwriting Style Samples")
    print("=" * 70)
    print()

    if not os.path.exists('sample.pdf'):
        print("Error: sample.pdf not found. Run create_sample_pdf.py first.")
        return

    styles = [
        {
            'name': 'Classic Blue Ink',
            'output_dir': 'samples/classic_blue',
            'settings': {
                'font_size': 28,
                'line_spacing': 40,
                'text_color': (0, 0, 139),  # Dark blue
                'margin_left': 200,
                'margin_right': 200,
                'margin_top': 200,
                'margin_bottom': 200
            }
        },
        {
            'name': 'Large Bold Black',
            'output_dir': 'samples/large_bold',
            'settings': {
                'font_size': 34,
                'line_spacing': 48,
                'text_color': (0, 0, 0),  # Black
                'margin_left': 150,
                'margin_right': 150,
                'margin_top': 150,
                'margin_bottom': 150
            }
        },
        {
            'name': 'Compact Navy',
            'output_dir': 'samples/compact_navy',
            'settings': {
                'font_size': 24,
                'line_spacing': 35,
                'text_color': (25, 25, 112),  # Navy blue
                'margin_left': 180,
                'margin_right': 180,
                'margin_top': 180,
                'margin_bottom': 180
            }
        },
        {
            'name': 'Elegant Purple',
            'output_dir': 'samples/elegant_purple',
            'settings': {
                'font_size': 30,
                'line_spacing': 43,
                'text_color': (75, 0, 130),  # Indigo
                'margin_left': 220,
                'margin_right': 220,
                'margin_top': 220,
                'margin_bottom': 220
            }
        },
        {
            'name': 'Vintage Sepia',
            'output_dir': 'samples/vintage_sepia',
            'settings': {
                'font_size': 28,
                'line_spacing': 40,
                'text_color': (101, 67, 33),  # Brown
                'background_color': (255, 248, 220, 255),  # Cornsilk
                'margin_left': 200,
                'margin_right': 200,
                'margin_top': 200,
                'margin_bottom': 200
            }
        }
    ]

    for style in styles:
        print(f"Creating: {style['name']}...")
        try:
            converter = PDFToHandwriting(**style['settings'])
            output_paths = converter.convert(
                'sample.pdf',
                output_dir=style['output_dir'],
                output_prefix='handwriting'
            )
            print(f"  ✓ Saved to {style['output_dir']}/")
            print(f"  ✓ Created {len(output_paths)} image(s)")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()

    print("=" * 70)
    print("All style samples created!")
    print("Check the 'samples/' directory to see different styles.")
    print("=" * 70)


if __name__ == "__main__":
    create_style_samples()
