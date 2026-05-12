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


app = FastAPI(title="ScholarChat API")

app.include_router(auth_router)
app.include_router(health_router)
app.include_router(documents_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "ScholarChat API Running"}


# Set up rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)