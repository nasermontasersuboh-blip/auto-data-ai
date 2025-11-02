from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from models import InvoiceFields
from extractors import pdf_bytes_to_text, extract_invoice_fields

app = FastAPI(title="auto-data-ai", version="0.1.0")

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <body>
            <h2>🚀 Auto Data AI API is running!</h2>
            <p>Visit <a href='/docs'>/docs</a> to use the API.</p>
        </body>
    </html>
    """

@app.post("/extract", response_class=JSONResponse)
async def extract_invoice(file: UploadFile = File(...)):
    content = await file.read()
    text = pdf_bytes_to_text(content)
    fields = extract_invoice_fields(text)
    return fields
