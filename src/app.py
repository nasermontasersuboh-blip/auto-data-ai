from fastapi import FastAPI, File, UploadFile
from extractors import pdf_bytes_to_text, extract_invoice_fields
import uvicorn

app = FastAPI(
    title="auto-data-ai",
    version="1.0",
    description="A simple API for extracting text and invoice data from PDF files."
)

@app.get("/")
def index():
    return {"message": "Welcome to Auto Data AI"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    # Read PDF file
    pdf_bytes = await file.read()
    
    # Extract text
    text = pdf_bytes_to_text(pdf_bytes)
    
    # Extract invoice fields
    fields = extract_invoice_fields(text)
    
    return {
        "success": True,
        "fields": fields,
        "raw_text": text[:1000]  # limit preview
    }

# Run locally
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
