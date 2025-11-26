from fpdf import FPDF
from io import BytesIO
import os

def create_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Path to UTF-8 font
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")

    # Register UTF-8 safe font
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Add text
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Output PDF to bytes
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

    return buffer
