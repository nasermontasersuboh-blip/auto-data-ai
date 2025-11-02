import re

def find_vendor(text: str) -> str:
    # Try "Invoice from" pattern -> else first non-empty line
    m = re.search(r'(?i)(?:invoice\s+from|from)\s*[:\-]?\s*(.+)', text)
    if m:
        return m.group(1).strip()
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return ""

def find_date(text: str) -> str:
    # Common formats: 2025-11-02, 02/11/2025, 02-11-2025, Nov 2, 2025
    patterns = [
        r'\b\d{4}-\d{2}-\d{2}\b',
        r'\b\d{2}/\d{2}/\d{4}\b',
        r'\b\d{2}-\d{2}-\d{4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s+\d{4}\b',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(0)
    return ""

def find_total(text: str) -> str:
    # Look for "Total" or "Amount Due" with a number
    m = re.search(r'(?i)(?:total|amount\s+due)\D*([0-9]{1,3}(?:[, ]?[0-9]{3})*(?:\.[0-9]{2})?)', text)
    return m.group(1) if m else ""

def find_currency(text: str) -> str:
    # Try symbol first, then ISO codes
    symbols = {'$':'USD', '€':'EUR', '£':'GBP', '₹':'INR', '¥':'JPY', '₽':'RUB', '₩':'KRW', '₪':'ILS', 'د.أ':'JOD'}
    for sym, code in symbols.items():
        if sym in text:
            return code
    m = re.search(r'\b(USD|EUR|GBP|INR|JPY|AUD|CAD|CHF|CNY|SAR|AED|JOD)\b', text, re.I)
    return m.group(1).upper() if m else ""
