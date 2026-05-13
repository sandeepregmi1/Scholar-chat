from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    upload_status: str
    owner_id: int

    pages: Optional[int] = None

    title: Optional[str] = None

    author: Optional[str] = None

    file_size: Optional[int] = None

    created_at: datetime

    class Config:
        from_attributes = True