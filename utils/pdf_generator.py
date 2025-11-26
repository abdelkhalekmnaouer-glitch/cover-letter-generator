from fpdf import FPDF
from io import BytesIO
import os

def create_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Path to Arial TTF
    font_path = os.path.join(os.path.dirname(__file__), "Arial.ttf")

    # Add Unicode-safe Arial
    pdf.add_font("ArialUnicode", "", font_path, uni=True)
    pdf.set_font("ArialUnicode", size=12)

    # Write the content
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Export to buffer
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
