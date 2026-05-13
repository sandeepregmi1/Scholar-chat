from app.services.llm_service import LLMService


class QuizService:

    def __init__(self):
        self.llm = LLMService()

    def generate_quiz(self, topic: str, chunks: list):

        context = "\n".join([c["chunk_text"] for c in chunks])

        prompt = f"""
You are an AI educational assistant.

Create a quiz with 5 multiple-choice questions.

Rules:
- Use ONLY the provided context
- Each question must have 4 options (A, B, C, D)
- Provide correct answer

Format STRICTLY like this:

Q1: question
A) option
B) option
C) option
D) option
Answer: B

Context:
{context}

Topic:
{topic}
"""

        return self.llm.generate(prompt)