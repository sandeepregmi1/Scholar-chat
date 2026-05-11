# app/services/vector_store.py
from app.services.chunking_service import chunk_text
from app.services.embedding_service import generate_embedding
from app.models.embedding import Embedding


class VectorStore:

    def __init__(self, db):
        self.db = db

    def process_and_store(self, document_id: int, text: str, page_number: int = None):

        if not text:
            return 0

        chunks = chunk_text(text)

        records = []

        for chunk in chunks:
            vector = list(generate_embedding(chunk))

            record = Embedding(
                document_id=document_id,
                chunk_text=chunk,
                embedding=vector,
                page_number=page_number
            )

            records.append(record)

        try:
            self.db.add_all(records)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

        return len(records)