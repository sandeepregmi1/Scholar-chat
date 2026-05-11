# app/services/vector_store.py

from app.models.embedding import Embedding


class VectorStore:

    def __init__(self, db):
        self.db = db

    def store(self, document_id: int, chunks: list, embeddings: list):
        """
        Save chunks + embeddings into pgvector DB
        """

        records = []

        for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):

            record = Embedding(
                document_id=document_id,
                chunk_text=chunk,
                embedding=vector,
                page_number=None  # optional for later upgrade
            )

            records.append(record)

        self.db.add_all(records)
        self.db.commit()

        return len(records)