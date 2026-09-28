from backend.document_utils import export_txt, export_docx, export_pdf

def test_txt_export():
    assert export_txt(" Hello \\n") == b"Hello"

def test_docx_export():
    assert export_docx("Draft text", "Test Agreement").startswith(b"PK")

def test_pdf_export():
    assert export_pdf("Draft text", "Test Agreement").startswith(b"%PDF")
