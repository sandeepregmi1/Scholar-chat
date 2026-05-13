from app.services.embedding_service import generate_embedding


text = "Artificial intelligence is transforming industries."

embedding = generate_embedding(text)

print(f"Vector length: {len(embedding)}")

print(embedding[:10])