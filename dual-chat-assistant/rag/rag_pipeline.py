from llm.qwen_client import QwenClient
from llm.ollama_client import OllamaClient


def build_llm_client(backend: str):
    if backend == "qwen":
        return QwenClient()
    elif backend == "ollama":
        return OllamaClient()
    else:
        raise ValueError("未知后端")

def build_context(top_chunks):
    context_parts = []

    for item in top_chunks:
        if item.get("page") is not None:
            header = f"[来源: {item['source']} | page: {item['page']} | chunk_id: {item['chunk_id']}]"
        else:
            header = f"[来源: {item['source']} | chunk_id: {item['chunk_id']}]"

        context_parts.append(f"{header}\n{item['content']}")

    return "\n\n".join(context_parts)

def build_rag_messages(query: str, context: str):
    system_prompt = (
        "你是一个基于给定资料回答问题的助手。"
        "请严格依据提供的资料回答，不要补充资料之外的事实。"
        "如果资料不足，请明确说：根据当前提供的资料，无法确定。"
    )

    user_prompt = f"""请基于以下资料回答问题。

资料：
{context}

问题：
{query}

要求：
1. 只依据资料回答
2. 先直接回答，再简要说明依据
3. 不要编造资料中不存在的信息
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def generate_rag_answer(query: str, top_chunks, backend: str = "qwen"):
    client = build_llm_client(backend)
    context = build_context(top_chunks)
    messages = build_rag_messages(query, context)
    return client.chat(messages)