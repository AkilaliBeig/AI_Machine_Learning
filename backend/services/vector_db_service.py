#from backend.vector_store import VectorStore
from ..vector_store import VectorStore


class VectorDBService:
    def __init__(self):
        self.store = VectorStore()

    def add_documents(self, chunks):
        for c in chunks:
            self.store.add_document(
                text=c["text"],
                metadata=c["metadata"]
            )

    def search(self, query: str, top_k: int = 3):
        return self.store.search(query, top_k)
