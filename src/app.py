from fastapi import FastAPI UploadFile File
from fastapiresponses import HTMLResponse JSONResponse
from .models import InvoiceFields
from .extractors import pdf_bytes_to_text, extract_invoice_fields

app = FastAPI(title="auto-data-ai", version="0.1.0")

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
      <head><title>auto-data-ai — Invoice Extractor (MVP)</title></head>
      <body style='font-family: system-ui; max-width: 760px; margin: 40px auto;'>
        <h1>Invoice Extractor (MVP)</h1>
        <p>Upload a <b>PDF invoice</b> to extract vendor, date, total, and currency.</p>
        <form action="/extract" method="post" enctype="multipart/form-data">
          <input type="file" name="pdf" accept="application/pdf" required />
          <button type="submit">Extract</button>
        </form>
      </body>
    </html>
    """

@app.post("/extract")
async def extract(pdf: UploadFile = File(...)):
    if pdf.content_type not in ("application/pdf",):
        return JSONResponse(status_code=400, content={"success": False, "message": "Please upload a PDF file."})

    pdf_bytes = await pdf.read()
    text = pdf_bytes_to_text(pdf_bytes)
    vendor, date, total, currency = extract_invoice_fields(text)

    return {
        "success": True,
        "fields": {"vendor": vendor, "date": date, "total": total, "currency": currency},
        "raw_text": text[:5000],
    }
App.py
