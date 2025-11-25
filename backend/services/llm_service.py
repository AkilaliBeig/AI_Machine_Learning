# backend/services/llm_service.py
from groq import Groq  # not GroqClient

class LLMService:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def generate_answer(self, query: str, context: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
        response = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content.strip()
