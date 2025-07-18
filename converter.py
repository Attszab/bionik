import fitz
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT

# 🔍 PDF-ből szöveg kinyerés bekezdésekkel
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        page_text = page.get_text("text")  # Tartalmaz sortöréseket
        if page_text:
            text += page_text + "\n"
    doc.close()
    return text

# 🧠 Bionic átalakítás: szavak első fele félkövér, bekezdésenként
def bionic_transform(text):
    def transform_word(word):
        split = len(word) // 2
        return f"<b>{word[:split]}</b>{word[split:]}"
    
    paragraphs = []
    for block in text.split("\n\n"):  # bekezdések
        words = re.findall(r'\w+|\W+', block)
        transformed = [transform_word(w) if w.strip().isalpha() else w for w in words]
        paragraphs.append("".join(transformed))
    return paragraphs  # lista bekezdésekkel

# 🖨️ PDF generálás bekezdésenként, XHTML formázással
def create_bionic_pdf(paragraphs, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm)

    style = ParagraphStyle(
        name="Bionic",
        fontName="Times-Bold",
        fontSize=12,
        leading=16,
        alignment=TA_LEFT
    )

    story = []
    for para in paragraphs:
        story.append(Paragraph(para, style))
        story.append(Spacer(1, 12))  # térköz a bekezdések között

    doc.build(story)

# 🚀 Fő konvertáló függvény
def bionic_pdf_converter(input_pdf, output_pdf):
    raw_text = extract_text_from_pdf(input_pdf)
    bionic_paragraphs = bionic_transform(raw_text)
    create_bionic_pdf(bionic_paragraphs, output_pdf)
