from io import BytesIO

from docx import Document
from docx.shared import Inches, Pt
from fpdf import FPDF


def export_txt(text: str) -> bytes:
    """
    Export text as UTF-8 bytes.

    Handles both actual newline characters and literal '\\n' or '\\r\\n'
    sequences, then removes whitespace from the beginning and end.
    """
    cleaned = (text or "")
    cleaned = cleaned.replace("\\r\\n", "\n")
    cleaned = cleaned.replace("\\n", "\n")
    return cleaned.strip().encode("utf-8")


def export_docx(
    text: str,
    title: str = "LegalEase Draft",
    logo_bytes: bytes | None = None,
) -> bytes:
    """Create a DOCX document from the supplied draft text."""
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)

    if logo_bytes:
        try:
            doc.add_picture(BytesIO(logo_bytes), width=Inches(1.4))
        except Exception:
            pass

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)

    doc.add_heading(title, 0)

    for line in (text or "").splitlines():
        line = line.strip()

        if not line:
            continue

        if len(line) < 100 and (
            line.isupper()
            or (line[:1].isdigit() and "." in line[:8])
        ):
            doc.add_heading(line, level=2)
        else:
            doc.add_paragraph(line)

    section.footer.paragraphs[0].text = (
        "LegalEase - AI-generated draft - Qualified legal review required"
    )

    output = BytesIO()
    doc.save(output)
    return output.getvalue()


def export_pdf(text: str, title: str = "LegalEase Draft") -> bytes:
    """Create a PDF document from the supplied draft text."""
    pdf = FPDF()

    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(18, 18, 18)

    pdf.set_font("Times", "B", 16)
    pdf.multi_cell(0, 9, title)
    pdf.ln(3)

    pdf.set_font("Times", size=11)

    normalized_text = (text or "")
    normalized_text = normalized_text.replace("\\r\\n", "\n")
    normalized_text = normalized_text.replace("\\n", "\n")

    for paragraph in normalized_text.split("\n"):
        if paragraph.strip():
            safe = paragraph.encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 6, safe)
            pdf.ln(1)

    pdf.set_y(-15)
    pdf.set_font("Times", size=8)
    pdf.cell(
        0,
        8,
        "LegalEase - AI-generated draft - Legal review required",
        align="C",
    )

    return bytes(pdf.output())