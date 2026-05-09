from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router

# Rate limiting imports
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


app = FastAPI(title="ScholarChat API")

app.include_router(auth_router)
app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "ScholarChat API Running"}


# Set up rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)