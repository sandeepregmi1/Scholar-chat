from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.vector_search import VectorSearch
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService

router = APIRouter(
    prefix="/multi-chat",
    tags=["Multi Document Chat"]
)


@router.post("/ask")
def ask_multi(
    question: str,
    document_ids: str = None,
    db: Session = Depends(get_db)
):

    ids = None
    if document_ids:
        ids = [int(x.strip()) for x in document_ids.split(",")]

    searcher = VectorSearch(db)
    prompt_builder = PromptService()
    llm = LLMService()

    chunks = searcher.search(
        query=question,
        document_ids=ids,
        top_k=5
    )

    prompt = prompt_builder.build_prompt(
        question=question,
        chunks=chunks
    )

    answer = llm.generate(prompt)

    return {
        "question": question,
        "documents_used": ids,
        "answer": answer,
        "sources": chunks
    }