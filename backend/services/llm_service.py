from groq import Groq

class LLMService:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    # 🔹 Used for final answer generation
    def generate_answer(self, query: str, context: str) -> str:
        prompt = f"""
Answer the question using ONLY the context below.
If the answer is not present, say so clearly.

Context:
{context}

Question:
{query}
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=200
        )

        if not response.choices:
            raise RuntimeError("No response from Groq")

        return response.choices[0].message.content.strip()

    # 🔹 Used ONLY for YES / NO checks
    def generate_raw(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10
        )

        if not response.choices:
            raise RuntimeError("No response from Groq")

        return response.choices[0].message.content.strip()
