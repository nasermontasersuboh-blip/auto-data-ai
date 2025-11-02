# src/extractors.py
from utils import find_currency, find_date, find_total, find_vendor
import fitz  # PyMuPDF for PDF processing

def pdf_bytes_to_text(pdf_bytes: bytes) -> str:
    """Extract text from a PDF file (in bytes)."""
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text")
    return text

def extract_invoice_fields(text: str):
    """Extract key fields (vendor, date, total, currency) from text."""
    vendor = find_vendor(text)
    date = find_date(text)
    total = find_total(text)
    currency = find_currency(text)
    return vendor, date, total, currency
