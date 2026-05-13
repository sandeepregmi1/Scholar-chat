# /app/api/v1/citations.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.vector_search import VectorSearch
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService

router = APIRouter(
    prefix="/citations",
    tags=["Citations"]
)


@router.post("/ask")
def ask_with_citations(
    question: str,
    document_id: int = None,
    db: Session = Depends(get_db)
):
    searcher = VectorSearch(db)
    prompt_builder = PromptService()
    llm = LLMService()

    # ✅ FIX: consistent vector search input
    document_ids = [document_id] if document_id else None

    chunks = searcher.search(
        query=question,
        document_ids=document_ids,
        top_k=3
    )

    prompt = prompt_builder.build_prompt(
        question=question,
        chunks=chunks
    )

    answer = llm.generate(prompt)

    # ✅ safe mapping (chunks already structured from VectorSearch)
    citations = [
        {
            "document_id": c.get("document_id"),
            "page_number": c.get("page_number"),
            "score": c.get("score")
        }
        for c in chunks
    ]

    return {
        "question": question,
        "answer": answer,
        "citations": citations
    }