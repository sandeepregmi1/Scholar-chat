from sqlalchemy import text
from app.services.embedding_service import generate_embedding

class VectorSearch:

    def __init__(self, db):
        self.db = db

    def search(self, query: str, document_id: int = None, top_k: int = 5):

        # 1. Convert query → embedding
        query_vector = generate_embedding(query)

        # 2. Convert to string format for SQL
        query_vector_str = str(query_vector)

        # 3. Build SQL
        sql = text("""
            SELECT 
                chunk_text,
                document_id,
                1 - (embedding <=> :query_vector) AS score
            FROM embeddings
            WHERE (:document_id IS NULL OR document_id = :document_id)
            ORDER BY embedding <=> :query_vector
            LIMIT :top_k
        """)

        # 4. Execute query
        result = self.db.execute(
            sql,
            {
                "query_vector": query_vector_str,
                "document_id": document_id,
                "top_k": top_k
            }
        )

        return [
            {
                "chunk_text": row.chunk_text,
                "document_id": row.document_id,
                "score": float(row.score)
            }
            for row in result.fetchall()
        ]