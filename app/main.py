from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router

app = FastAPI(title="ScholarChat API")

app.include_router(auth_router)
app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "ScholarChat API Running"}