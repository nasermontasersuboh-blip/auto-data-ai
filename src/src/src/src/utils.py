import re
from typing import Optional

CURRENCY_REGEX = r"(?i)(USD|EUR|GBP|JOD|SAR|AED|QAR|KWD|BHD|OMR|EGP|TRY|MAD)"
DATE_REGEX = r"(?i)(\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4})"
TOTAL_REGEX = r"(?i)(total|amount due|grand total)[^\d]*(\d+[.,]\d{2})"

VENDOR_HINTS = [
    r"(?i)(invoice\s*from|seller|vendor|company)[:\s]*([\w\-&'\\.\\s]{2,})",
]

def find_currency(text: str) -> Optional[str]:
    m = re.search(CURRENCY_REGEX, text)
    return m.group(1).upper() if m else None

def find_date(text: str) -> Optional[str]:
    m = re.search(DATE_REGEX, text)
    return m.group(1) if m else None

def find_total(text: str) -> Optional[float]:
    m = re.search(TOTAL_REGEX, text)
    if m:
        try:
            return float(m.group(2).replace(',', ''))
        except ValueError:
            return None
    return None

def find_vendor(text: str) -> Optional[str]:
    for pattern in VENDOR_HINTS:
        m = re.search(pattern, text)
        if m:
            return m.group(2).strip()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if lines:
        return lines[0][:120]
    return None
