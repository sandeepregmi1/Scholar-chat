from app.services.llm_service import LLMService


class NotesService:

    def __init__(self):
        self.llm = LLMService()

    def generate_notes(self, topic: str, chunks: list):

        context = "\n".join([c["chunk_text"] for c in chunks])

        prompt = f"""
You are an academic assistant.

Generate study notes for the topic: {topic}

Use ONLY the provided document context.

Context:
{context}

Format:
1. Summary
2. Bullet Notes
3. Key Concepts
"""

        return self.llm.generate(prompt)