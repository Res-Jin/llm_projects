from llm.qwen_client import QwenClient
from llm.ollama_client import OllamaClient
from config import MAX_HISTORY_MESSAGES, SYSTEM_PROMPT


def choose_backend():
    while True:
        print("\n请选择模型后端：")
        print("1. Qwen API")
        print("2. Ollama Local")
        choice = input("输入 1 或 2：").strip()

        if choice == "1":
            return "qwen"
        elif choice == "2":
            return "ollama"
        else:
            print("输入无效，请重新选择。")


def build_client(backend: str):
    if backend == "qwen":
        return QwenClient()
    elif backend == "ollama":
        return OllamaClient()
    else:
        raise ValueError("未知后端")


def trim_messages(messages, max_history_messages):
    system_message = messages[0]
    history = messages[1:]

    if len(history) > max_history_messages:
        history = history[-max_history_messages:]

    return [system_message] + history


def main():
    print("=== Dual Chat Assistant v0.2 ===")
    backend = choose_backend()
    client = build_client(backend)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print(f"\n当前后端: {backend}")
    print("输入 exit 退出程序。\n")

    while True:
        user_input = input("你：").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("程序结束。")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        messages = trim_messages(messages, MAX_HISTORY_MESSAGES)

        try:
            print("助手：", end="", flush=True)
            reply = client.stream_chat(messages)
            messages.append({"role": "assistant", "content": reply})
            messages = trim_messages(messages, MAX_HISTORY_MESSAGES)
            print()
        except Exception as e:
            print(f"\n请求失败：{e}\n")


if __name__ == "__main__":
    main()