from pydantic import BaseModel
from typing import Optional

class InvoiceFields(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[str] = None
    currency: Optional[str] = None
