import re
from typing import Optional

# naive patterns; adjust later if you want better accuracy
VENDOR_PAT = re.compile(r"(?im)^\s*(invoice\s+from|vendor)\s*:\s*(.+)$")
DATE_PAT   = re.compile(r"(?i)\b(?:date|invoice date)\b[:\s]*([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})")
TOTAL_PAT  = re.compile(r"(?i)\b(total|amount due)\b[:\s]*([0-9]+(?:[.,][0-9]{2})?)")
CURR_PAT   = re.compile(r"(?i)\b(usd|eur|gbp|\$|€|£)\b")

def _clean(s: Optional[str]) -> Optional[str]:
    if not s: return s
    return s.strip().strip(":").strip()

def find_vendor(text: str) -> Optional[str]:
    m = VENDOR_PAT.search(text)
    return _clean(m.group(2) if m else None)

def find_date(text: str) -> Optional[str]:
    m = DATE_PAT.search(text)
    return _clean(m.group(1) if m else None)

def find_total(text: str) -> Optional[str]:
    m = TOTAL_PAT.search(text)
    return _clean(m.group(2) if m else None)

def find_currency(text: str) -> Optional[str]:
    m = CURR_PAT.search(text)
    return _clean(m.group(1) if m else None)
