import requests
from config import OLLAMA_BASE_URL, OLLAMA_EMBED_MODEL

class OllamaEmbeddingClient:
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL.rstrip("/")
        self.model = OLLAMA_EMBED_MODEL

    def embed_texts(self, texts):
        url = f"{self.base_url}/api/embed"
        payload = {
            "model": self.model,
            "input": texts,
        }

        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["embeddings"]
    
    def embed_query(self, text):
        embeddings = self.embed_texts([text])
        return embeddings[0]