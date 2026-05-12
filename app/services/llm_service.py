# /home/sandeep/Projects/ScholarChat /app/services/llm_service.py

import requests
import json


class LLMService:

    def __init__(self, model="phi3"):
        self.model = model

    def generate_stream(self, prompt: str):
        """
        Stream response from Ollama token by token
        """

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))

                if "response" in data:
                    yield data["response"]