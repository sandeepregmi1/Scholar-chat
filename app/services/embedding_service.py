# /home/sandeep/Projects/ScholarChat /app/services/embedding_service.py
from sentence_transformers import SentenceTransformer

# Load once globally (VERY IMPORTANT for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):
    """
    Convert text into vector embedding (384-dim)
    """
    return model.encode(text).tolist()


def generate_embeddings_batch(texts: list[str]):
    """
    Faster batch embedding (important for chunking)
    """
    vectors = model.encode(texts)
    return [v.tolist() for v in vectors]