from fpdf import FPDF
from io import BytesIO
import os
import unicodedata
import re

# --- Utility to clean problematic unicode (emoji, zero-width, etc.) ---
def clean_text(text):
    cleaned = "".join(
        ch for ch in text 
        if not unicodedata.category(ch).startswith("So")
    )
    cleaned = cleaned.replace("\u200b", "")
    cleaned = cleaned.replace("\xa0", " ")
    cleaned = re.sub(r"[ ]{2,}", " ", cleaned)
    return cleaned


class LetterPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()

    def add_header_block(self, text, font_path):
        # Upper-left coordinates block
        self.set_xy(20, 20)
        self.set_font("ArialUnicode", size=12)
        for line in text.split("\n"):
            self.cell(0, 6, line, ln=True)

    def add_subject(self, subject, font_path):
        self.ln(5)
        self.set_font("ArialUnicode", style="B", size=12)
        self.cell(0, 8, f"Objet : {subject}", ln=True)
        self.ln(3)

    def add_paragraph(self, text):
        self.set_font("ArialUnicode", size=12)
        self.multi_cell(0, 8, text)
        self.ln(3)


def create_pdf(full_text):
    # FONT PATH
    font_path = os.path.join(os.path.dirname(__file__), "arial.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError("arial.ttf not found in utils/ directory.")

    # Clean text to avoid FPDF width errors
    full_text = clean_text(full_text)

    # Split content according to expected structure
    lines = full_text.strip().split("\n")

    # Build blocks
    header_lines = []
    subject_line = ""
    body_lines = []

    # Reconstruct intelligent structure:
    # First 5 lines = coordinate block
    # Line starting with "Objet" → subject
    # Rest = paragraphs

    i = 0
    # Coordinates (first non-empty 4–6 lines)
    while i < len(lines) and lines[i].strip() != "":
        header_lines.append(lines[i])
        i += 1

    # Find subject
    for j in range(i, len(lines)):
        if lines[j].lower().startswith("objet"):
            subject_line = lines[j].replace("Objet :", "").strip()
            i = j + 1
            break

    # Remaining = body paragraphs
    body_lines = [line for line in lines[i:] if line.strip() != ""]

    # Generate PDF
    pdf = LetterPDF()

    # Register Arial UTF-8 font
    pdf.add_font("ArialUnicode", "", font_path, uni=True)
    pdf.set_font("ArialUnicode", size=12)

    # Add header block
    pdf.add_header_block("\n".join(header_lines), font_path)

    # Add subject
    pdf.add_subject(subject_line, font_path)

    # Add salutation (mandatory)
    pdf.add_paragraph("Madame, Monsieur,")

    # Add paragraphs
    for para in body_lines:
        pdf.add_paragraph(para)

    # Final polite sentence if absent
    # (Your generated text usually contains one but we ensure consistency)
    if not body_lines[-1].lower().startswith("je vous remercie"):
        pdf.add_paragraph("Je vous remercie pour l’attention portée à ma candidature.")

    # Output to bytes for Streamlit
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
