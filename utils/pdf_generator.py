from fpdf import FPDF
from io import BytesIO
import os
import unicodedata
import re

# --- CLEANING ---
def clean_text(text):
    cleaned = "".join(
        ch for ch in text
        if not unicodedata.category(ch).startswith("So")  # remove emojis
    )
    cleaned = cleaned.replace("\u200b", "")
    cleaned = cleaned.replace("\xa0", " ")
    cleaned = re.sub(r"[ ]{2,}", " ", cleaned)
    return cleaned


# --- PDF CLASS ULTRA FIDÈLE ---
class UltraFidelePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        self.set_margins(left=20, top=20, right=20)

    def add_coordonnees(self, lines):
        self.set_xy(20, 20)
        self.set_font("ArialReg", size=11)
        for line in lines:
            self.cell(0, 6, line, ln=True)  # EXACT spacing 6 pts

    def add_objet(self, text):
        self.ln(4)  # espace avant objet
        self.set_font("ArialBold", size=12)
        self.cell(0, 8, f"Objet : {text}", ln=True)
        self.ln(3)  # espace après objet

    def add_salutation(self):
        self.ln(2)
        self.set_font("ArialReg", size=12)
        self.cell(0, 8, "Madame, Monsieur,", ln=True)
        self.ln(2)

    def add_paragraph(self, text):
        self.set_font("ArialReg", size=12)
        self.multi_cell(0, 7, text)  # interligne contenu
        self.ln(1.5)  # espacement après paragraphe


# --- GENERATE PDF ---
def create_pdf(text):
    # Clean text
    text = clean_text(text)

    # Load fonts
    base_dir = os.path.dirname(__file__)
    font_reg = os.path.join(base_dir, "arial.ttf")
    font_bold = os.path.join(base_dir, "arialbd.ttf")

    if not os.path.exists(font_reg):
        raise FileNotFoundError("arial.ttf missing in utils/")
    if not os.path.exists(font_bold):
        raise FileNotFoundError("arialbd.ttf missing in utils/")

    pdf = UltraFidelePDF()

    # Register fonts
    pdf.add_font("ArialReg", "", font_reg, uni=True)
    pdf.add_font("ArialBold", "", font_bold, uni=True)

    # --- PARSE STRUCTURED LETTER ---
    # The AI must return text using the tags:
    # @@coordonnees, @@objet, @@salutation, @@p1, @@p2, @@p3, @@p4, @@signature

    sections = {
        "coordonnees": [],
        "objet": "",
        "p": [],
        "signature": "",
    }

    lines = text.split("\n")
    current = None

    for line in lines:
        line = line.strip()
        if line.startswith("@@coordonnees"):
            current = "coordonnees"
            continue
        elif line.startswith("@@objet"):
            current = "objet"
            continue
        elif line.startswith("@@p"):
            m = re.match(r"@@p(\d+)", line)
            if m:
                current = "p"
                continue
        elif line.startswith("@@signature"):
            current = "signature"
            continue

        if current == "coordonnees" and line:
            sections["coordonnees"].append(line)

        elif current == "objet":
            if line:
                sections["objet"] = line

        elif current == "p":
            if line:
                sections["p"].append(line)

        elif current == "signature" and line:
            sections["signature"] = line

    # --- BUILD PDF ULTRA FIDÈLE ---
    pdf.add_coordonnees(sections["coordonnees"])
    pdf.add_objet(sections["objet"])
    pdf.add_salutation()

    for paragraph in sections["p"]:
        pdf.add_paragraph(paragraph)

    # signature
    if sections["signature"]:
        pdf.add_paragraph(sections["signature"])

    # Output
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
