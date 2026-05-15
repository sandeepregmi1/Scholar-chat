# /home/sandeep/Projects/ScholarChat/backend/app/api/v1/chat.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_user

from app.models.user import User

from app.services.vector_search import VectorSearch
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService
from app.services.chat_history_service import ChatHistoryService
from app.services.cache_service import CacheService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

cache = CacheService()


@router.post("/ask")
def ask_question(
    question: str,
    document_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    searcher = VectorSearch(db)
    prompt_builder = PromptService()
    llm = LLMService()
    history_service = ChatHistoryService(db)

    # -------------------------
    # STEP 1: Save user message (ALWAYS)
    # -------------------------
    history_service.save_message(
        user_id=current_user.id,
        document_id=document_id,
        role="user",
        content=question
    )

    # -------------------------
    # STEP 2: Check cache (AFTER saving user message)
    # -------------------------
    cached_answer = cache.get(current_user.id, document_id or 0, question)

    if cached_answer:
        # still save assistant response to DB for consistency
        history_service.save_message(
            user_id=current_user.id,
            document_id=document_id,
            role="assistant",
            content=cached_answer
        )

        return StreamingResponse(
            iter([cached_answer]),
            media_type="text/plain"
        )

    # -------------------------
    # STEP 3: Load conversation history
    # -------------------------
    history = history_service.get_recent_messages(
        user_id=current_user.id,
        document_id=document_id,
        limit=10
    )

    # -------------------------
    # STEP 4: Vector search
    # -------------------------
    document_ids = [document_id] if document_id else None

    chunks = searcher.search(
        query=question,
        document_ids=document_ids,
        top_k=3
    )

    # -------------------------
    # STEP 5: Build prompt
    # -------------------------
    prompt = prompt_builder.build_prompt(
        question=question,
        chunks=chunks,
        history=history
    )

    # -------------------------
    # STEP 6: Generate response
    # -------------------------
    answer = llm.generate(prompt)

    # -------------------------
    # STEP 7: Save assistant response
    # -------------------------
    history_service.save_message(
        user_id=current_user.id,
        document_id=document_id,
        role="assistant",
        content=answer
    )

    # -------------------------
    # STEP 8: Cache response
    # -------------------------
    cache.set(
        current_user.id,
        document_id or 0,
        question,
        answer,
        ttl=3600
    )

    # -------------------------
    # STEP 9: Return response
    # -------------------------
    return StreamingResponse(
        iter([answer]),
        media_type="text/plain"
    )