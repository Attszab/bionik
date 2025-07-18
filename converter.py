import fitz
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT

# 🔍 PDF-ből szöveg kinyerés bekezdésekkel
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        page_text = page.get_text("text")  # Ez tartalmaz sortöréseket is
        if page_text:
            text += page_text + "\n"
    doc.close()
    return text

# 🧠 Bionic átalakítás, bekezdésenként
def bionic_transform(text):
    def transform_word(word):
        split = len(word) // 2
        return f"<b>{word[:split]}</b>{word[split:]}"
    
    final = []
    for paragraph in text.split("\n\n"):
        words = re.findall(r'\w+|\W+', paragraph)
        transformed = [transform_word(w) if w.strip().isalpha() else w for w in words]
        final.append("".join(transformed))
    return "<br/><br/>".join(final)

# 🖨️ PDF generálás XHTML formázással
def create_bionic_pdf(text, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm)

    style = ParagraphStyle(
        name="Bionic",
        fontName="Times-Roman",
        fontSize=12,
        leading=16,
        alignment=TA_LEFT
    )

    story = [Paragraph(text, style)]
    doc.build(story)

# 🚀 Konvertáló hívás
def bionic_pdf_converter(input_pdf, output_pdf):
    raw_text = extract_text_from_pdf(input_pdf)
    bionic_text = bionic_transform(raw_text)
    create_bionic_pdf(bionic_text, output_pdf)
