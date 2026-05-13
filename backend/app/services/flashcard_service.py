from app.services.llm_service import LLMService


class FlashcardService:

    def __init__(self):
        self.llm = LLMService()

    def generate_flashcards(self, topic: str, chunks: list):
        context = "\n".join([chunk["chunk_text"] for chunk in chunks])

        prompt = f"""
You are an educational AI assistant.

Using ONLY the provided context, generate 5 flashcards.

Format:
Q: question
A: answer

Context:
{context}

Topic:
{topic}
"""

        return self.llm.generate(prompt)