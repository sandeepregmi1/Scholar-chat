from app.services.chunking_service import chunk_text


sample_text = "Hello world " * 500

chunks = chunk_text(sample_text)

print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):

    print(f"\n--- CHUNK {i+1} ---\n")

    print(chunk[:200])