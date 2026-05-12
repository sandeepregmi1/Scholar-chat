#  /home/sandeep/Projects/ScholarChat /app/api/v1/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.vector_search import VectorSearch
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/ask")
def ask_question(
    question: str,
    document_id: int = None,
    db: Session = Depends(get_db)
):

    try:
        # Services
        searcher = VectorSearch(db)
        prompt_builder = PromptService()
        llm = LLMService()

        # 1. Retrieve relevant chunks (RAG step 1)
        chunks = searcher.search(
            query=question,
            document_id=document_id,
            top_k=3
        )

        # 2. Build prompt (RAG step 2)
        prompt = prompt_builder.build_prompt(
            question=question,
            chunks=chunks
        )

        # 3. Generate answer (RAG step 3)
        answer = llm.generate(prompt)

        # 4. Clean response (avoid leaking prompt in production later)
        return {
            "question": question,
            "retrieved_chunks": chunks,
            "answer": answer
            
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Chat request failed"
        }