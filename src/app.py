from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from extractors import pdf_bytes_to_text, extract_invoice_fields

app = FastAPI(title="auto-data-ai", version="1.0")

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!doctype html><html><body style="font-family:sans-serif;padding:24px">
      <h1>Auto Data AI</h1>
      <p><a href="/docs">Open API Docs</a> • <a href="/health">Health</a></p>
    </body></html>
    """

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = pdf_bytes_to_text(pdf_bytes)
    vendor, date, total, currency = extract_invoice_fields(text)
    return {"success": True, "fields": {
        "vendor": vendor, "date": date, "total": total, "currency": currency
    }, "raw_text": text[:1000]}
