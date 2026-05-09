# app/api/v1/documents.py

import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.core.deps import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# FILE VALIDATION SETTINGS

ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

UPLOAD_STATUS_UPLOADED = "uploaded"
UPLOAD_STATUS_PROCESSING = "processing"
UPLOAD_STATUS_READY = "ready"
UPLOAD_STATUS_FAILED = "failed"


# FILE UPLOAD ENDPOINT

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # VALIDATE FILE EXTENSION

    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOCX, and TXT files are allowed"
        )

    # READ FILE CONTENT

    content = await file.read()

    # VALIDATE FILE SIZE

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large (max 20MB)"
        )

    # CREATE UPLOAD DIRECTORY

    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    # GENERATE UNIQUE FILENAME

    unique_filename = f"{uuid.uuid4()}{ext}"

    file_path = os.path.join(upload_dir, unique_filename)

    # SAVE FILE LOCALLY

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    
        
  


    # =========================
    # CREATE DATABASE ENTRY
    # =========================

    new_document = Document(
        filename=file.filename,
        file_path=file_path,
        upload_status=UPLOAD_STATUS_UPLOADED,
        owner_id=current_user.id
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)


    # =========================
    # PROCESS DOCUMENT
    # =========================

    try:

        # uploaded → processing
        new_document.upload_status = UPLOAD_STATUS_PROCESSING

        db.commit()
        db.refresh(new_document)

        # ==================================
        # FUTURE AI PROCESSING GOES HERE
        # ==================================

        # Example:
        # - extract text
        # - embeddings
        # - vector DB

        # processing success
        new_document.upload_status = UPLOAD_STATUS_READY

        db.commit()
        db.refresh(new_document)

    except Exception:

        # processing failed
        new_document.upload_status = UPLOAD_STATUS_FAILED

        db.commit()
        db.refresh(new_document)

        raise HTTPException(
            status_code=500,
            detail="Document processing failed"
        )
 
    return new_document 

# GET MY DOCUMENTS


@router.get("/my", response_model=list[DocumentResponse])
def get_my_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    docs = db.query(Document).filter(
        Document.owner_id == current_user.id
    ).all()

    return [
        {
            "id": d.id,
            "filename": d.filename,
            "file_path": d.file_path,
            "upload_status": d.upload_status,
            "owner_id": d.owner_id,
            "created_at": d.created_at
        }
        for d in docs
    ]