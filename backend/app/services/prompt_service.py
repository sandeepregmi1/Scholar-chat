# app/services/prompt_service.py

class PromptService:

    def build_prompt(self, question: str, chunks: list):

        context = "\n\n".join(
            [chunk["chunk_text"] for chunk in chunks]
        )

        prompt = f"""
You are an AI assistant for answering questions from uploaded documents.

Use ONLY the provided context.

RULES:
- Use ONLY the provided context.
- Do NOT add external knowledge.
- Do NOT create citations, sources, or references.
- If answer is not in context, say:
  "I could not find the answer in the uploaded document."

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

        prompt = f"""You are a professional AI Research Assistant.

You MUST respond in a structured format.

STRICT OUTPUT FORMAT:

## Summary
Provide a short overview (3–4 lines)

## Key Findings
- Bullet points of important facts from documents

## Comparison Table
Create a simple comparison:

| Aspect | Document 1 | Document 2 | ............
|--------|------------|------------|
| Yield | ... | ... |
| Cost | ... | ... |
| Accuracy | ... | ... |

## Insights
Explain patterns, similarities, and differences clearly

## Conclusion
Final 2–3 line conclusion

RULES:
- Use ONLY provided context
- Do NOT add external knowledge
- Use exact numbers from documents
- Be concise and structured

Context:
{context}

Research Question:
{question}

Detailed Analysis:
"""
        return prompt