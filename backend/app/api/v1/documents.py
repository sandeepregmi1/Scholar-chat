# /home/sandeep/Projects/ScholarChat /app/api/v1/documents.py
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

from app.services.document_pipeline import DocumentPipeline


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# =========================
# SETTINGS
# =========================

ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

UPLOAD_STATUS_UPLOADED = "uploaded"
UPLOAD_STATUS_PROCESSING = "processing"
UPLOAD_STATUS_READY = "ready"
UPLOAD_STATUS_FAILED = "failed"


# =========================
# UPLOAD ENDPOINT
# =========================

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -------------------------
    # VALIDATE EXTENSION
    # -------------------------
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOCX, and TXT files are allowed"
        )

    # -------------------------
    # READ FILE
    # -------------------------
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large (max 20MB)"
        )

    # -------------------------
    # SAVE FILE LOCALLY
    # -------------------------
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(upload_dir, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    # -------------------------
    # CREATE DB ENTRY (uploaded)
    # -------------------------
    document = Document(
        filename=file.filename,
        file_path=file_path,
        upload_status=UPLOAD_STATUS_UPLOADED,
        owner_id=current_user.id,
        file_size=len(content)
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # =========================
    # PROCESS PIPELINE
    # =========================
    try:
        # update status → processing
        document.upload_status = UPLOAD_STATUS_PROCESSING
        db.commit()

        pipeline = DocumentPipeline(db)

        result = pipeline.run(
            file_path=file_path,
            document=document,
            ext=ext,
            content=content
        )

        cleaned_text = result["text"]
        metadata = result["metadata"]

        document.content = cleaned_text[:5000]

        # -------------------------
        # (FOR PHASE 5 READY HOOK)
        # -------------------------
        # At this point you will plug:
        # - chunking
        # - embeddings
        # - vector DB storage

        # mark ready
        document.upload_status = UPLOAD_STATUS_READY
        db.commit()

    except Exception as e:
        document.upload_status = UPLOAD_STATUS_FAILED
        db.commit()

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )

    return document


# =========================
# GET USER DOCUMENTS
# =========================

@router.get("/my", response_model=list[DocumentResponse])
def get_my_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    docs = db.query(Document).filter(
        Document.owner_id == current_user.id
    ).all()

    return docs