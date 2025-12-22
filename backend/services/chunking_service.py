class TextSplitter:
    def __init__(self, chunk_size=500, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text: str, filename: str):
        chunks = []
        start = 0
        chunk_id = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "source": filename,
                        "chunk_id": chunk_id
                    }
                })
                chunk_id += 1

            start = end - self.overlap

        return chunks
