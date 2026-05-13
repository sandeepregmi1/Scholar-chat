from app.services.search_service import SearchService

service = SearchService()

results = service.search("online learning", top_k=3)

for r in results:
    print(r["score"], r["chunk_text"])