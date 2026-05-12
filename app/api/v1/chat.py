# app/api/v1/chat.py

from fastapi import APIRouter
from app.services.vector_search import VectorSearch
from app.services.prompt_service import PromptService
from app.db.session import SessionLocal

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/ask")
def ask_question(question: str):

    db = SessionLocal()

    searcher = VectorSearch(db)
    prompt_builder = PromptService()

    chunks = searcher.search(
        query=question,
        top_k=3
    )

    prompt = prompt_builder.build_prompt(
        question=question,
        chunks=chunks
    )

    return {
        "question": question,
        "prompt": prompt
    }