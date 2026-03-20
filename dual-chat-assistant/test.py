from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("QWEN_API_KEY")
base_url = os.getenv("QWEN_BASE_URL")
model = os.getenv("QWEN_MODEL", "qwen-plus")

print("正在测试：")
print("BASE_URL =", base_url)
print("MODEL    =", model)

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

try:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个简洁的助手。"},
            {"role": "user", "content": "请回复：API测试成功"}
        ],
        temperature=0
    )
    print("\n调用成功：")
    print(resp.choices[0].message.content)
except Exception as e:
    print("\n调用失败：")
    print(type(e).__name__, str(e))