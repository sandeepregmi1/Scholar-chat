# /app/api/v1/quiz.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.vector_search import VectorSearch
from app.services.quiz_service import QuizService

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


@router.post("/generate")
def generate_quiz(
    topic: str,
    document_id: int = None,
    db: Session = Depends(get_db)
):

    searcher = VectorSearch(db)
    quiz_service = QuizService()

    # ✅ FIX: convert single ID → list
    document_ids = [document_id] if document_id else None

    chunks = searcher.search(
        query=topic,
        document_ids=document_ids,
        top_k=3
    )

    quiz = quiz_service.generate_quiz(
        topic=topic,
        chunks=chunks
    )

    return {
        "topic": topic,
        "quiz": quiz
    }