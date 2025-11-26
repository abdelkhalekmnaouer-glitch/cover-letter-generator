from fpdf import FPDF
from io import BytesIO
import os
import re
import unicodedata

def clean_text(text):
    # Remove emojis and very wide unicode symbols
    cleaned = "".join(
        ch for ch in text 
        if not unicodedata.category(ch).startswith("So")  # "Symbol, Other"
    )

    # Remove zero-width chars
    cleaned = cleaned.replace("\u200b", "")

    # Replace non-breaking spaces
    cleaned = cleaned.replace("\xa0", " ")

    # Replace multiple spaces
    cleaned = re.sub(r"\s+", " ", cleaned)

    # Keep newlines intact
    cleaned = cleaned.replace(" .", ".")

    return cleaned


def create_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Clean text BEFORE writing
    text = clean_text(text)

    # Load custom Arial font
    font_path = os.path.join(os.path.dirname(__file__), "arial.ttf")

    if not os.path.exists(font_path):
        raise FileNotFoundError("arial.ttf not found in utils/ directory.")

    pdf.add_font("ArialUnicode", "", font_path, uni=True)
    pdf.set_font("ArialUnicode", size=12)

    # Write PDF content
    for line in text.split("\n"):
        if line.strip():  # avoid empty oversized lines
            pdf.multi_cell(0, 10, line)
        else:
            pdf.ln(5)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
