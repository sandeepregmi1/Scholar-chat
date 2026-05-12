# app/api/v1/chat.py


from fastapi import APIRouter
from app.services.vector_search import VectorSearch
from app.db.session import SessionLocal

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/ask")
def ask_question(question: str):

    db = SessionLocal()

    searcher = VectorSearch(db)

    results = searcher.search(
        query=question,
        top_k=3
    )

    return {
        "question": question,
        "retrieved_chunks": results
    }