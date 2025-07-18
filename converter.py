import fitz
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def bionic_transform(text):
    def transform_word(word):
        split = len(word) // 2
        return f"<b>{word[:split]}</b>{word[split:]}"
    
    words = re.findall(r'\w+|\W+', text)
    transformed = [transform_word(w) if w.strip().isalpha() else w for w in words]
    return "".join(transformed)

from reportlab.lib.styles import ParagraphStyle

def create_bionic_pdf(text, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    style = ParagraphStyle(name="Bionic", fontName="Times-Roman", fontSize=12, leading=16)

    # A szöveg tartalmaz <b>...</b> tageket → XHTML formázás
    story = [Paragraph(text, style)]

    doc.build(story)

def bionic_pdf_converter(input_pdf, output_pdf):
    raw_text = extract_text_from_pdf(input_pdf)
    bionic_text = bionic_transform(raw_text)
    create_bionic_pdf(bionic_text, output_pdf)
