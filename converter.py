import fitz
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT

# 🔍 Bekezdés-alapú szövegkinyerés a PDF-ből
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    paragraphs = []
    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: b[1])  # Fentről lefelé (Y koordináta)
        for block in blocks:
            block_text = block[4].strip()
            if block_text:
                paragraphs.append(block_text)
    doc.close()
    return "\n\n".join(paragraphs)

# 🧠 Bionic kiemelés: szavak első fele félkövér
def bionic_transform(text):
    def transform_word(word):
        split = len(word) // 2
        return f"<b>{word[:split]}</b>{word[split:]}"
    
    paragraphs = []
    for block in text.split("\n\n"):  # bekezdésenként
        words = re.findall(r'\w+|\W+', block)
        transformed = [transform_word(w) if w.strip().isalpha() else w for w in words]
        paragraphs.append("".join(transformed))
    return paragraphs

# 🖨️ PDF generálás: bekezdésenkénti Paragraph + másfeles sortávolság
def create_bionic_pdf(paragraphs, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm)

    style = ParagraphStyle(
        name="Bionic",
        fontName="Helvetica",
        fontSize=12,
        leading=18,  # másfeles sortávolság
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
