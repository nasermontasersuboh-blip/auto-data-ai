# src/utils.py
import re
from typing import Optional

CURRENCY_MAP = {
    "$": "USD", "€": "EUR", "£": "GBP", "JOD": "JOD", "د.أ": "JOD",
    "USD": "USD", "EUR": "EUR", "GBP": "GBP", "SAR": "SAR", "AED": "AED"
}

def _to_number(s: str) -> Optional[float]:
    if not s: 
        return None
    s = s.strip()
    # normalize 1,234.56 / 1 234,56 / 1.234,56 -> 1234.56
    s = s.replace(" ", "")
    if s.count(",") > 0 and s.count(".") == 0:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None

def find_currency(text: str) -> Optional[str]:
    # look for explicit codes first
    m = re.search(r"\b(USD|EUR|GBP|SAR|AED|JOD)\b", text, re.I)
    if m:
        return m.group(1).upper()
    # then symbols near total/amount
    m = re.search(r"(?:total|amount due|grand total)[^\n]{0,30}?([€$£])", text, re.I)
    if m:
        return CURRENCY_MAP.get(m.group(1))
    # any symbol anywhere
    m = re.search(r"[€$£]", text)
    if m:
        return CURRENCY_MAP.get(m.group(0))
    return None

def find_total(text: str) -> Optional[float]:
    # prefer labeled totals
    patterns = [
        r"(?:grand\s*total|amount\s*due|total)\s*[:\-]?\s*([€$£]?\s?[\d.,]+)",
        r"([€$£]\s?[\d.,]+)\s*(?:grand\s*total|amount\s*due|total)"
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return _to_number(re.sub(r"[€$£]", "", m.group(1)))
    # fallback: largest money-like number
    nums = [ _to_number(x) for x in re.findall(r"[€$£]?\s?[\d][\d.,]{2,}", text) ]
    nums = [n for n in nums if n is not None]
    return max(nums) if nums else None

def find_date(text: str) -> Optional[str]:
    # common formats: 2025-11-02, 02/11/2025, 11/02/2025, 02 Nov 2025
    pats = [
        r"\b(20\d{2})-(\d{1,2})-(\d{1,2})\b",
        r"\b(\d{1,2})/(\d{1,2})/(20\d{2})\b",
        r"\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(20\d{2})\b"
    ]
    months = {m:i for i,m in enumerate(
        ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], start=1)}
    # ISO first
    m = re.search(pats[0], text)
    if m:
        y, mo, d = m.groups()
        return f"{int(y):04d}-{int(mo):02d}-{int(d):02d}"
    # dd/mm/yyyy or mm/dd/yyyy (we can’t be perfect; prefer dd/mm)
    m = re.search(pats[1], text)
    if m:
        a, b, y = m.groups()
        dd, mm = int(a), int(b)
        if dd > 12:  # treat as dd/mm
            return f"{int(y):04d}-{mm:02d}-{dd:02d}"
        # ambiguous: default to dd/mm
        return f"{int(y):04d}-{mm:02d}-{dd:02d}"
    # 02 Nov 2025
    m = re.search(pats[2], text, re.I)
    if m:
        d, mon, y = m.groups()
        return f"{int(y):04d}-{months[mon[:3].title()]:02d}-{int(d):02d}"
    return None

def find_vendor(text: str) -> Optional[str]:
    # take the first non-empty line that doesn’t look like “INVOICE”/labels
    for line in text.splitlines():
        l = line.strip()
        if not l: 
            continue
        if re.search(r"\b(invoice|bill|statement|tax|date|total|amount)\b", l, re.I):
            continue
        # skip lines that are mostly numbers
        if len(re.sub(r"[^\d]", "", l)) > len(l) * 0.5:
            continue
        return l[:120]
    return None
