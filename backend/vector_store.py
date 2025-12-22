import faiss
import numpy as np
from fastembed import TextEmbedding

class VectorStore:
    def __init__(self):
        self.model = TextEmbedding()
        self.index = faiss.IndexFlatL2(384)
        self.documents = []

    def embed(self, text: str):
        for emb in self.model.embed([text]):
            return np.array(emb, dtype="float32")

    def add_document(self, text: str, metadata: dict):
        emb = self.embed(text)
        self.index.add(np.array([emb]))
        self.documents.append({
            "text": text,
            "metadata": metadata
        })

    def search(self, query: str, top_k=3):
        if len(self.documents) == 0:
            return []

        q_emb = self.embed(query)
        D, I = self.index.search(np.array([q_emb]), top_k)

        results = []
        seen = set()

        for idx, dist in zip(I[0], D[0]):
            if idx < len(self.documents):
                text = self.documents[idx]["text"]
                if text not in seen:
                    results.append({
                        "document": self.documents[idx],
                        "score": float(dist)
                    })
                    seen.add(text)

        return results

