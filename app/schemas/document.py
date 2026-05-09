from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    upload_status: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True