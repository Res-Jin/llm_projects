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
        context_parts.append(
            f"[来源: {item['source']} | chunk_id: {item['chunk_id']}]\n{item['content']}"
        )

    return "\n\n".join(context_parts)


def build_rag_messages(query: str, context: str):
    system_prompt = (
        "你是一个基于给定资料回答问题的助手。"
        "请严格依据提供的资料回答，不要凭空编造。"
        "如果资料中没有足够信息，请明确说“根据当前提供的资料，无法确定”。"
    )

    user_prompt = f"""请基于以下资料回答问题。

资料：
{context}

问题：
{query}

要求：
1. 先直接回答问题
2. 回答尽量简洁清晰
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
    answer = client.chat(messages)
    return answer