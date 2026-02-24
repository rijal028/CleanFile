import streamlit as st
from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from io import BytesIO
import re

st.set_page_config(page_title="CleanFile", page_icon="🔒")

st.title("🔒 CleanFile")
st.write("Upload a PDF and rebuild it into a clean, script-free version.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])


# =========================
# TEXT NORMALIZATION
# =========================
def normalize_text(text):
    if not text:
        return ""

    text = text.replace("■", "")
    text = text.replace("/equals", "=")

    # Remove excessive spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# TEXT EXTRACTION
# =========================
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    pages_text = []

    for page in reader.pages:
        try:
            text = page.extract_text(extraction_mode="layout")
        except TypeError:
            text = page.extract_text()

        if text:
            pages_text.append(text)
        else:
            pages_text.append("")

    return pages_text


# =========================
# REBUILD SAFE PDF
# =========================
def rebuild_pdf(text_pages):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    main_title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        alignment=1
    )

    heading_style = ParagraphStyle(
        'HeadingCustom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        'NormalLeft',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14
    )

    first_line_used_as_title = False

    for text in text_pages:
        lines = text.split("\n")

        for line in lines:
            clean_line = normalize_text(line)

            if not clean_line:
                elements.append(Spacer(1, 0.15 * inch))
                continue

            # First meaningful line → main title
            if not first_line_used_as_title:
                elements.append(Paragraph(clean_line, main_title_style))
                elements.append(Spacer(1, 0.3 * inch))
                first_line_used_as_title = True
                continue

            # ===== Improved Heading Detection =====
            word_count = len(clean_line.split())

            is_heading = (
                len(clean_line) < 80 and
                word_count <= 12 and
                not clean_line.endswith(".") and
                clean_line.upper() == clean_line
            )

            if is_heading:
                elements.append(Paragraph(clean_line, heading_style))
            else:
                elements.append(Paragraph(clean_line, normal_style))

        elements.append(Spacer(1, 0.4 * inch))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# =========================
# MAIN FLOW
# =========================
if uploaded_file:
    st.info("Extracting text...")

    try:
        text_pages = extract_text_from_pdf(uploaded_file)

        if not any(text_pages):
            st.error("No readable text found in this PDF.")
        else:
            st.success("Text extracted.")
            st.info("Rebuilding script-free document...")

            clean_pdf_buffer = rebuild_pdf(text_pages)

            st.success("Done. Your clean document is ready.")

            st.download_button(
                label="Download Clean PDF",
                data=clean_pdf_buffer,
                file_name="cleaned_document.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Processing error: {e}")