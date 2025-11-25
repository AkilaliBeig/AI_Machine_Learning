import faiss
import numpy as np
from fastembed import TextEmbedding

class VectorStore:
    def __init__(self):
        self.model = TextEmbedding()
        self.index = faiss.IndexFlatL2(384)   # 384 dims for fastembed
        self.documents = []

    def embed(self, text: str):
        # FastEmbed generates embeddings lazily (generator)
        for emb in self.model.embed([text]):
            return np.array(emb, dtype="float32")

    def add_document(self, text: str):
        embedding = self.embed(text)
        self.index.add(np.array([embedding]))
        self.documents.append(text)

    def search(self, query: str, top_k: int = 3):
        query_emb = self.embed(query)
        D, I = self.index.search(np.array([query_emb]), top_k)

        results = []
        for idx, dist in zip(I[0], D[0]):
            if idx < 0 or idx >= len(self.documents):
                continue
            results.append({
                "document": self.documents[idx],
                "score": float(dist)
            })
        return results
