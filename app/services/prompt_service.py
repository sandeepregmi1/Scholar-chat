# app/services/prompt_service.py

class PromptService:

    def build_prompt(self, question: str, chunks: list):

        context = "\n\n".join(
            [chunk["chunk_text"] for chunk in chunks]
        )

        prompt = f"""
You are an AI assistant for answering questions from uploaded documents.

Use ONLY the provided context.

If answer is not found in context, say:
"I could not find the answer in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

        return prompt