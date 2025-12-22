# backend/services/rag_service.py
from .vector_db_service import VectorDBService
from .llm_service import LLMService

class RAGService:
    def __init__(self, vector_service: VectorDBService, llm_service: LLMService):
        self.vector_service = vector_service
        self.llm_service = llm_service

    def query(self, user_query: str):
        results = self.vector_service.search(user_query, top_k=3)
        context = "\n".join([r["document"] for r in results])
        answer = self.llm_service.generate_answer(user_query, context)
        return {"query": user_query, "answer": answer, "retrieved_documents": results}
