# /home/sandeep/Projects/ScholarChat /app/services/vector_search.py

from sqlalchemy import text
from app.services.embedding_service import generate_embedding


class VectorSearch:

    def __init__(self, db):
        self.db = db

    def search(self, query: str, document_ids: list = None, top_k: int = 5):
            
        # Convert query → embedding

        query_vector = generate_embedding(query)
        
        # Convert to string format for SQL

        query_vector_str = str(query_vector)

        sql = text("""
            SELECT
                chunk_text,
                document_id,
                page_number,
                1 - (embedding <=> :query_vector) AS score
            FROM embeddings
            WHERE (
                :document_ids IS NULL
                OR document_id = ANY(:document_ids)
            )
            ORDER BY embedding <=> :query_vector
            LIMIT :top_k
        """)

        result = self.db.execute(
            sql,
            {
                "query_vector": query_vector_str,
                "document_ids": document_ids,
                "top_k": top_k
            }
        )

        return [
            {
                "chunk_text": row.chunk_text,
                "document_id": row.document_id,
                "page_number": row.page_number,
                "score": float(row.score)
            }
            for row in result.fetchall()
        ]