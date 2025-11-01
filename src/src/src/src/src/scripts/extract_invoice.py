import argparse
import json
from pathlib import Path
from src.extractors import pdf_bytes_to_text, extract_invoice_fields

def main():
    parser = argparse.ArgumentParser(description="Extract fields from PDF invoice")
    parser.add_argument("--pdf", required=True, help="Path to a PDF invoice")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        raise SystemExit(f"File not found: {pdf_path}")

    text = pdf_bytes_to_text(pdf_path.read_bytes())
    vendor, date, total, currency = extract_invoice_fields(text)

    print(json.dumps({
        "vendor": vendor,
        "date": date,
        "total": total,
        "currency": currency,
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
