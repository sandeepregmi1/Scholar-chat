from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

from app.models.user import User


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ScholarChat API"
)


@app.get("/")
def root():
    return {
        "message": "ScholarChat API Running"
    }