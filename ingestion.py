from __future__ import annotations

from pathlib import Path


def extract_document_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        digital_text = _extract_pdf_text(path)
        if digital_text.strip():
            return digital_text
        return _ocr_pdf(path)
    if suffix in {".png", ".jpg", ".jpeg"}:
        return _ocr_image(path)
    raise ValueError(f"Unsupported file type: {suffix}")


def _extract_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = []
        for page_number, page in enumerate(reader.pages, start=1):
            pages.append(f"\n[PAGE {page_number}]\n{page.extract_text() or ''}")
        return "\n".join(pages)
    except Exception:
        return ""


def _ocr_pdf(path: Path) -> str:
    try:
        import fitz
        import pytesseract
        from PIL import Image

        doc = fitz.open(path)
        pages = []
        for page_number, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=220)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pages.append(f"\n[OCR PAGE {page_number}]\n{pytesseract.image_to_string(image)}")
        return "\n".join(pages)
    except Exception as exc:
        return f"[OCR failed or unavailable: {exc}]"


def _ocr_image(path: Path) -> str:
    try:
        import pytesseract
        from PIL import Image

        return pytesseract.image_to_string(Image.open(path))
    except Exception as exc:
        return f"[OCR failed or unavailable: {exc}]"

