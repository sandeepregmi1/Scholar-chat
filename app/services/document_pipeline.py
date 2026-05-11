# /home/sandeep/Projects/ScholarChat /app/services/document_pipeline.py

# app/services/document_pipeline.py

from app.services.document_processor import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_with_ocr,
    clean_extracted_text,
    extract_pdf_metadata,
    extract_docx_metadata
)

from app.services.embedding_service import generate_embedding
from app.services.chunking_service import chunk_text
from app.services.vector_store import VectorStore




class DocumentPipeline:

    def __init__(self, db):
        self.db = db

    def run(self, file_path, document, ext, content):

        # 1. Extract
        extracted_text = self.extract(file_path, ext, content)

        # 2. Metadata
        metadata = self.get_metadata(file_path, ext)

        # 3. Clean
        cleaned_text = clean_extracted_text(extracted_text)
        print(f"cleaned:  ",cleaned_text)



        # 4. Chunk
        chunks = chunk_text(cleaned_text)
        print(f"chunks: ",chunks)

        # 5. Embeddings
        embeddings = [
            generate_embedding(chunk) for chunk in chunks
        ]
        print(f"embeddings: ",embeddings)

        # 6. Store in vector DB
        vector_store = VectorStore(self.db)
        print(f"vec_store : ",vector_store)

        vector_store.store(
            document_id=document.id,
            chunks=chunks,
            embeddings=embeddings
        )

        return {
            "text": cleaned_text,
            "metadata": metadata,
            "chunks": len(chunks),
            "embeddings": len(embeddings)
        }

    def extract(self, file_path, ext, content):
        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
            if not text.strip():
                text = extract_text_with_ocr(file_path)
            return text

        if ext == ".docx":
            return extract_text_from_docx(file_path)

        if ext == ".txt":
            return content.decode("utf-8")

        return ""

    def get_metadata(self, file_path, ext):
        if ext == ".pdf":
            return extract_pdf_metadata(file_path)

        if ext == ".docx":
            return extract_docx_metadata(file_path)

        return {"pages": None, "title": None, "author": None}