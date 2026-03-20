from openai import OpenAI
from config import QWEN_API_KEY, QWEN_BASE_URL, QWEN_MODEL, TEMPERATURE

class QwenClient:
    def __init__(self):
        if not QWEN_API_KEY:
            raise ValueError("key未配置")
        if not QWEN_BASE_URL:
            raise ValueError("url未配置")
        
        self.client = OpenAI(
            api_key=QWEN_API_KEY,
            base_url=QWEN_BASE_URL
        )
        self.model = QWEN_MODEL
        self.temperature = TEMPERATURE

    def chat(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return response.choices[0].message.content
    
    def stream_chat(self, messages):
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=True
        )

        full_text = []
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                full_text.append(delta)

        print()
        return "".join(full_text)
