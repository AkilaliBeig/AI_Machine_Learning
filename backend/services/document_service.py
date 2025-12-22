# backend/services/document_service.py
import os

class DocumentService:
    def __init__(self, storage_dir="storage"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_document(self, filename: str, content: bytes) -> str:
        path = os.path.join(self.storage_dir, filename)
        with open(path, "wb") as f:
            f.write(content)

        return content.decode("utf-8")