#  /home/sandeep/Projects/ScholarChat /app/api/v1/chat.py

# /app/api/v1/chat.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
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

    searcher = VectorSearch(db)
    prompt_builder = PromptService()
    llm = LLMService()

    # 1. FIX: use document_ids (NOT document_id)
    document_ids = [document_id] if document_id else None

    chunks = searcher.search(
        query=question,
        document_ids=document_ids,
        top_k=3
    )

    # 2. Build prompt
    prompt = prompt_builder.build_prompt(
        question=question,
        chunks=chunks
    )

    # 3. Stream response
    return StreamingResponse(
        llm.generate_stream(prompt),
        media_type="text/plain"
    )