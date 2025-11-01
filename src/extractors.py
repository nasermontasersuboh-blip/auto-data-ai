from io import BytesIO
from typing import Tuple
from pdfminer.high_level import extract_text
from .utils import find_currency, find_date, find_total, find_vendor


def pdf_bytes_to_text(pdf_bytes: bytes) -> str:
    """Convert PDF bytes into readable text."""
    with BytesIO(pdf_bytes) as f:
        text = extract_text(f)
    return text or ""


def extract_invoice_fields(text: str) -> Tuple[str, str, float, str]:
    """Extract key invoice fields (vendor, date, total, currency)."""
    vendor = find_vendor(text)
    date = find_date(text)
    total = find_total(text)
    currency = find_currency(text)
    return vendor, date, total, currency
