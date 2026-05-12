import requests 


class LLMService:

    def __init__(self, model="phi3"):
        self.model = model

    def generate(self, prompt: str):

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]