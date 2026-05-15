# app/services/prompt_service.py

class PromptService:


    def build_prompt(
        self,
        question: str,
        chunks: list,
        history: list = None
    ):
        # document context
        context = "\n\n".join(
            [chunk["chunk_text"] for chunk in chunks]
        )

        # previous conversation
        conversation = ""

        if history:
            conversation = "\n".join(
                [f"{msg.role}: {msg.content}" for msg in history]
            )

        prompt = f"""
You are ScholarChat, an AI assistant for answering questions from uploaded documents.

Use ONLY the provided document context.

RULES:
- Use ONLY the provided context.
- Use previous conversation for follow-up understanding.
- Do NOT add external knowledge.
- Do NOT create citations, sources, or references.
- If answer is not in context, say:
  "I could not find the answer in the uploaded document."

Previous conversation:
{conversation}

Context:
{context}

Question:
{question}

Answer:
"""
        return prompt

    def build_research_prompt(self, question: str, chunks: list):

        context = "\n\n".join(
            [chunk["chunk_text"] for chunk in chunks]
        )

        prompt = f"""You are an AI research assistant.

Analyze the uploaded documents and answer ONLY using the provided context.

RULES:
- Compare information across documents.
- Include exact numerical values where available.
- Highlight similarities and differences.
- Do NOT invent facts.
- Do NOT use outside knowledge.
- If information is missing, say so clearly.


Context:
{context}

Research Question:
{question}

Detailed Analysis:
"""
        return prompt