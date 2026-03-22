#!/usr/bin/env python3
"""
Test script demonstrating the programmatic API of PDF to Handwriting converter.
"""

from pdf_to_handwriting import PDFToHandwriting


def test_api():
    """Test the programmatic API."""
    print("=" * 60)
    print("Testing PDF to Handwriting Converter - Python API")
    print("=" * 60)

    # Test 1: Basic conversion with default settings
    print("\n[Test 1] Basic conversion with default settings...")
    converter1 = PDFToHandwriting()
    try:
        output_paths = converter1.convert('sample.pdf', output_dir='api_test_1')
        print(f"✓ Success! Created {len(output_paths)} image(s)")
        for path in output_paths:
            print(f"  - {path}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 2: Custom settings
    print("\n[Test 2] Custom settings (larger font, blue ink)...")
    converter2 = PDFToHandwriting(
        font_size=32,
        line_spacing=45,
        text_color=(0, 0, 255),
        margin_left=150,
        margin_right=150,
        margin_top=150,
        margin_bottom=150
    )
    try:
        output_paths = converter2.convert('sample.pdf', output_dir='api_test_2', output_prefix='blue_ink')
        print(f"✓ Success! Created {len(output_paths)} image(s)")
        for path in output_paths:
            print(f"  - {path}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 3: Error handling - non-existent file
    print("\n[Test 3] Error handling - non-existent file...")
    converter3 = PDFToHandwriting()
    try:
        output_paths = converter3.convert('nonexistent.pdf')
        print(f"✗ Should have raised an error!")
    except FileNotFoundError as e:
        print(f"✓ Correctly caught error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    # Test 4: Text extraction only
    print("\n[Test 4] Text extraction only...")
    converter4 = PDFToHandwriting()
    try:
        text = converter4.extract_text_from_pdf('sample.pdf')
        print(f"✓ Extracted {len(text)} characters")
        print(f"  First 100 chars: {text[:100]}...")
    except Exception as e:
        print(f"✗ Error: {e}")

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_api()
