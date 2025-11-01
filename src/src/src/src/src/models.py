from pydantic import BaseModel
from typing import Optional

class InvoiceFields(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    currency: Optional[str] = None

class ExtractResponse(BaseModel):
    success: bool
    fields: InvoiceFields
    raw_text: Optional[str] = None
    message: Optional[str] = None
