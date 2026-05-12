from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.db.session import SessionLocal
from app.services.vector_search import VectorSearch
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService

router = APIRouter(tags=["WebSocket Chat"])


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    db = SessionLocal()
    searcher = VectorSearch(db)
    prompt_builder = PromptService()
    llm = LLMService()

    try:
        while True:
            question = await websocket.receive_text()

            chunks = searcher.search(query=question, top_k=3)

            prompt = prompt_builder.build_prompt(
                question=question,
                chunks=chunks
            )

            for token in llm.generate_stream(prompt):
                await websocket.send_text(token)

            await websocket.send_text("[END]")

    except WebSocketDisconnect:
        db.close()