# backend/services/vector_db_service.py
#from backend.vector_store import VectorStore
from ..vector_store import VectorStore


class VectorDBService:
    def __init__(self):
        self.store = VectorStore()

    def add_document(self, text: str):
        self.store.add_document(text)

    def search(self, query: str, top_k: int = 3):
        return self.store.search(query, top_k=top_k)
