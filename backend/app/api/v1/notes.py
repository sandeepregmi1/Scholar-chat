# /app/api/v1/notes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.vector_search import VectorSearch
from app.services.notes_service import NotesService

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.post("/generate")
def generate_notes(
    topic: str,
    document_id: int = None,
    db: Session = Depends(get_db)
):

    searcher = VectorSearch(db)
    notes_service = NotesService()

    # ✅ FIX: convert single id → list
    document_ids = [document_id] if document_id else None

    chunks = searcher.search(
        query=topic,
        document_ids=document_ids,
        top_k=5
    )

    notes = notes_service.generate_notes(
        topic=topic,
        chunks=chunks
    )

    return {
        "topic": topic,
        "notes": notes
    }