from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from extractors import pdf_bytes_to_text, extract_invoice_fields

app = FastAPI(title="auto-data-ai", version="0.1.0")

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <h1>Auto-Data AI</h1>
    <p>Upload an invoice via <a href="/docs">/docs</a>.</p>
    """

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = pdf_bytes_to_text(pdf_bytes)
    vendor, date, total, currency = extract_invoice_fields(text)
    return {
        "success": True,
        "fields": {
            "vendor": vendor,
            "date": date,
            "total": total,
            "currency": currency
        },
        "raw_text": text[:5000]
    }
