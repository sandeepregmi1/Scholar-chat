from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router

# Rate limiting imports
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.v1.documents import router as documents_router

from app.api.v1.chat import router as chat_router

from app.api.v1 import ws_chat

from app.api.v1 import notes

from app.api.v1.flashcards import router as flashcards_router

from app.api.v1.quiz import router as quiz_router




app = FastAPI(title="ScholarChat API")

app.include_router(auth_router)
app.include_router(health_router)
app.include_router(documents_router)

app.include_router(chat_router)

app.include_router(ws_chat.router)


app.include_router(notes.router)

app.include_router(flashcards_router)


app.include_router(quiz_router)



@app.get("/")
def root():
    return {"message": "ScholarChat API Running"}


# Set up rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)