from fastapi import FastAPI, UploadFile, File

class InvoiceFields:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self):
        return {"text": self.text}
