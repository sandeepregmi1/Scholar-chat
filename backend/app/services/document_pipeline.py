# app/services/document_pipeline.py

from app.services.document_processor import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_with_ocr,
    clean_extracted_text,
    extract_pdf_metadata,
    extract_docx_metadata
)

from app.services.vector_store import VectorStore


class DocumentPipeline:

    def __init__(self, db):
        self.db = db

    def run(self, file_path, document, ext, content):

        # 1. Extract text
        extracted_text = self.extract(file_path, ext, content)

        # 2. Extract metadata
        metadata = self.get_metadata(file_path, ext)

        # 3. Clean text
        cleaned_text = clean_extracted_text(extracted_text)

        print("cleaned text:", cleaned_text)

        # 4. Process + Store vectors
        vector_store = VectorStore(self.db)

        stored_chunks = vector_store.process_and_store(
            document_id=document.id,
            text=cleaned_text
        )

        print("stored chunks:", stored_chunks)

        return {
            "text": cleaned_text,
            "metadata": metadata,
            "chunks": stored_chunks
        }

    def extract(self, file_path, ext, content):

        if ext == ".pdf":

            text = extract_text_from_pdf(file_path)

            # fallback OCR
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

        return {
            "pages": None,
            "title": None,
            "author": None
        }