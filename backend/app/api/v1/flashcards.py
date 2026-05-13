# /app/api/v1/flashcards.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.vector_search import VectorSearch
from app.services.flashcard_service import FlashcardService

router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcards"]
)


@router.post("/generate")
def generate_flashcards(
    topic: str,
    document_id: int = None,
    db: Session = Depends(get_db)
):
    searcher = VectorSearch(db)
    flashcard_service = FlashcardService()

    # ✅ FIX: convert to list format
    document_ids = [document_id] if document_id else None

    chunks = searcher.search(
        query=topic,
        document_ids=document_ids,
        top_k=3
    )

    flashcards = flashcard_service.generate_flashcards(
        topic=topic,
        chunks=chunks
    )

    return {
        "topic": topic,
        "flashcards": flashcards
    }