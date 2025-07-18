import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def create_bionic_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    margin_left = 20 * mm
    margin_top = height - 30 * mm
    x = margin_left
    y = margin_top
    line_height = 14

    words = text.split()

    for word in words:
        # Bionic hatás: első 40% félkövér
        split_index = max(1, int(len(word) * 0.4))
        bold_part = word[:split_index]
        normal_part = word[split_index:]

        # Félkövér rész (Times-Bold)
        c.setFont("Times-Bold", 12)
        c.drawString(x, y, bold_part)

        bold_width = pdfmetrics.stringWidth(bold_part, "Times-Bold", 12)

        # Normál rész (Times-Roman)
        c.setFont("Times-Roman", 12)
        c.drawString(x + bold_width, y, normal_part)

        word_width = bold_width + pdfmetrics.stringWidth(normal_part, "Times-Roman", 12)
        x += word_width + 4  # szóköz

        # Sortörés, ha túlmegy a margón
        if x > width - margin_left:
            x = margin_left
            y -= line_height

    c.save()

def bionic_pdf_converter(input_path, output_path):
    text = extract_text_from_pdf(input_path)
    create_bionic_pdf(text, output_path)
