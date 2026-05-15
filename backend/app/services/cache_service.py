import redis
import hashlib
import json


class CacheService:
    def __init__(self):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

    def make_key(self, user_id: int, document_id: int, question: str):
        raw = f"{user_id}:{document_id}:{question.strip().lower()}"
        return "chat:" + hashlib.md5(raw.encode()).hexdigest()

    def get(self, user_id: int, document_id: int, question: str):
        key = self.make_key(user_id, document_id, question)
        return self.client.get(key)

    def set(self, user_id: int, document_id: int, question: str, value: str, ttl: int = 3600):
        key = self.make_key(user_id, document_id, question)
        self.client.setex(key, ttl, value)