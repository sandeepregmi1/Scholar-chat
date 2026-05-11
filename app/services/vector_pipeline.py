# /home/sandeep/Projects/ScholarChat /app/services/vector_pipeline.py
from app.services.chunking_service import chunk_text
from app.services.embedding_service import generate_embeddings_batch


def build_embeddings_from_text(text: str):
    """
    1. chunk text
    2. generate embeddings
    3. return structured data
    """

    chunks = chunk_text(text)

    embeddings = generate_embeddings_batch(chunks)

    results = []

    for i in range(len(chunks)):
        results.append({
            "chunk_text": chunks[i],
            "embedding": embeddings[i],
            "chunk_index": i
        })

    return results