# /home/sandeep/Projects/ScholarChat /app/api/v1/search.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.vector_search import VectorSearch

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/")
def search_documents(
    query: str,
    document_id: int = None,
    db: Session = Depends(get_db)
):

    searcher = VectorSearch(db)

    results = searcher.search(
        query=query,
        document_id=document_id,
        top_k=5
    )

    return {
        "query": query,
        "results": results
    }