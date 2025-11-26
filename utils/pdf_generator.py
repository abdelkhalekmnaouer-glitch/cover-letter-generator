from fpdf import FPDF
from io import BytesIO

def create_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    # Add content line by line
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)

    # Save into buffer
    buffer = BytesIO()
    pdf.output(buffer, "F")
    buffer.seek(0)
    return buffer
