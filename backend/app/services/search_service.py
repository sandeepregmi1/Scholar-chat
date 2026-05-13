# /home/sandeep/Projects/ScholarChat/app/services/search_service.py

from sqlalchemy import text
from app.services.embedding_service import generate_embedding
from app.db.session import SessionLocal


class SearchService:

    def __init__(self):
        self.db = SessionLocal()

    def search(self, query: str, top_k: int = 5, document_id: int = None):

        # Generate embedding
        vector = generate_embedding(query)

        # Convert Python list → pgvector string format
        vector_str = str(vector)

        sql = """
            SELECT 
                chunk_text,
                page_number,
                document_id,
                1 - (embedding <=> CAST(:vec AS vector)) AS score
            FROM embeddings
        """

        params = {
            "vec": vector_str,
            "k": top_k
        }

        # Optional document filtering
        if document_id:
            sql += " WHERE document_id = :doc_id"
            params["doc_id"] = document_id

        sql += """
            ORDER BY embedding <=> CAST(:vec AS vector)
            LIMIT :k
        """

        result = self.db.execute(text(sql), params)

        return [
            {
                "chunk_text": row.chunk_text,
                "score": float(row.score),
                "page_number": row.page_number,
                "document_id": row.document_id
            }
            for row in result.fetchall()
        ]