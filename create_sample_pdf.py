#!/usr/bin/env python3
"""
Create a sample PDF for testing the PDF to Handwriting converter.
"""

from fpdf import FPDF
import os


def create_sample_pdf(output_path: str = "sample.pdf"):
    """
    Create a sample PDF with some text for testing.

    Args:
        output_path: Path where the PDF will be saved
    """
    # Create instance of FPDF class
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Add title
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, text="Sample Document for PDF to Handwriting Converter", align='C')
    pdf.ln(15)

    # Add content
    pdf.set_font("Helvetica", size=12)

    content = """This is a sample PDF document created for testing the PDF to Handwriting converter tool.

The tool extracts text from PDF files and converts it into handwriting-style images that look natural and realistic.

Features:
- Accurate text extraction from PDFs
- Customizable font and styling options
- Automatic text wrapping and pagination
- High-quality image output

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump!

Testing numbers: 0123456789
Testing special characters: !@#$%^&*()_+-=[]{}|;:',.<>?/

This document contains enough text to demonstrate the wrapping and formatting capabilities of the converter tool."""

    # Write content
    pdf.multi_cell(0, 7, text=content)

    # Save the pdf
    pdf.output(output_path)
    print(f"Sample PDF created: {output_path}")


if __name__ == "__main__":
    create_sample_pdf("sample.pdf")
