import json
import requests
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE


class OllamaClient:
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL.rstrip("/")
        self.model = OLLAMA_MODEL
        self.temperature = TEMPERATURE

    def chat(self, messages):
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.temperature
            }
        }

        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        return data["message"]["content"]
    
    def stream_chat(self, messages):
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": self.temperature
            }
        }

        response = requests.post(url, json=payload, stream=True, timeout=120)
        response.raise_for_status()

        full_text = []

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line.decode("utf-8"))
            content = data.get("message", {}).get("content", "")

            if content:
                print(content, end="", flush=True)
                full_text.append(content)

        print()
        return "".join(full_text)