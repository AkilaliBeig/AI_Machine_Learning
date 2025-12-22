# backend/services/rag_service.py
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, vector_service, llm_service):
        self.vector_service = vector_service
        self.llm_service = llm_service

    def query(self, user_query: str):
        logger.info(f"Query received: {user_query}")

        # 1️⃣ Retrieve documents
        try:
            results = self.vector_service.search(user_query, top_k=3)
            logger.info(f"Vector search results: {results}")
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return {
                "query": user_query,
                "answer": f"Vector search failed: {e}",
                "retrieved_documents": []
            }

        if not results:
            return {
                "query": user_query,
                "answer": "No relevant information found in the document.",
                "retrieved_documents": []
            }

        # 2️⃣ Build context
        context_chunks = [
            r["document"]["text"]
            for r in results
            if r.get("document") and r["document"].get("text")
        ]
        context = "\n\n".join(context_chunks)
        logger.info(f"Context built:\n{context}")

        if not context.strip():
            return {
                "query": user_query,
                "answer": "No relevant textual context found in the document.",
                "retrieved_documents": results
            }

        # 3️⃣ Answerability check
        check_prompt = f"""
Context:
{context}

Question:
{user_query}

Can the question be reasonably answered using ONLY the information in the context,
even if it requires explanation, summarization, or inference?

Reply ONLY with YES or NO.
"""
        try:
            check_response = self.llm_service.generate_raw(check_prompt)
            logger.info(f"Answerability check response: {check_response}")
        except Exception as e:
            logger.error(f"LLM answerability check failed: {e}")
            return {
                "query": user_query,
                "answer": "LLM failed during answerability check.",
                "retrieved_documents": results
            }

        decision = (check_response or "").strip().upper()
        if "YES" not in decision:
            return {
                "query": user_query,
                "answer": "The provided document does not contain information to answer this question.",
                "retrieved_documents": results
            }

        # 4️⃣ Generate answer
        answer_prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{user_query}

Be clear, concise, and user-friendly.
"""
        try:
            answer = self.llm_service.generate_answer(user_query, context)
            logger.info(f"Answer generated: {answer}")
        except Exception as e:
            logger.error(f"LLM answer generation failed: {e}")
            return {
                "query": user_query,
                "answer": "LLM failed during answer generation.",
                "retrieved_documents": results
            }

        return {
            "query": user_query,
            "answer": answer,
            "retrieved_documents": results
        }
