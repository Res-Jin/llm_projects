from llm.qwen_client import QwenClient
from llm.ollama_client import OllamaClient
from config import MAX_HISTORY_MESSAGES, SYSTEM_PROMPT
from utils.chat_storage import (
    save_chat,
    load_chat,
    list_chat_sessions,
    rename_chat
)


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

def create_initial_messages(system_prompt: str):
    return [{"role": "system", "content": system_prompt}]

def print_help():
    print("\n可用命令：")
    print("/clear                   清空上下文")
    print("/history                 查看当前消息数")
    print("/backend                 切换模型后端")
    print("/system 新提示词          修改 system prompt")
    print("/sessions                列出历史会话")
    print("/load 文件名              加载历史会话")
    print("/save [文件名]            保存当前会话")
    print("/rename 新文件名          重命名当前会话")
    print("/help                    查看帮助")
    print("/exit                    退出程序\n")

def main():
    print("=== Dual Chat Assistant v0.3 ===")
    backend = choose_backend()
    client = build_client(backend)

    current_system_prompt = SYSTEM_PROMPT
    messages = create_initial_messages(current_system_prompt)
    current_session_filename = None

    print(f"\n当前后端: {backend}")
    print("输入 /help 查看命令。\n")

    while True:
        user_input = input("你：").strip()

        if not user_input:
            continue

        if user_input in {"/exit", "exit", "quit"}:
            try:
                saved_path = save_chat(
                    messages=messages,
                    backend=backend,
                    system_prompt=current_system_prompt,
                    filename=current_session_filename
                )
                if current_session_filename is None:
                    current_session_filename = saved_path.split("\\")[-1].split("/")[-1]
                print(f"聊天记录已保存到：{saved_path}")
            except Exception as e:
                print(f"退出前保存失败：{e}")

            print("程序结束。")
            break

        if user_input == "/help":
            print_help()
            continue

        if user_input == "/clear":
            messages = create_initial_messages(current_system_prompt)
            print("上下文已清空")
            continue

        if user_input == "/history":
            print(f"当前消息数（含 system）: {len(messages)}")
            print(f"当前普通历史消息数: {len(messages) - 1}")
            continue

        if user_input == "/backend":
            backend = choose_backend()
            client = build_client(backend)
            print(f"已切换到后端: {backend}")
            print("提示：当前上下文未清空，你正在把同一段历史交给新后端继续回答。")
            continue

        if user_input.startswith("/system"):
            new_prompt = user_input[len("/system "):].strip()
            if not new_prompt:
                print("system prompt 不能为空！")
                continue

            current_system_prompt = new_prompt
            messages = create_initial_messages(current_system_prompt)
            print("系统提示词已更新，并已重置上下文。")
            continue

        if user_input == "/sessions":
            sessions = list_chat_sessions()
            if not sessions:
                print("暂无历史对话")
            else:
                print("\n历史对话：")
                for idx, name in enumerate(sessions, start=1):
                    print(f"{idx}.{name}")
                print()
            continue

        if user_input.startswith("/load "):
            filename = user_input[len("/load "):].strip()
            if not filename:
                print("请输入要加载的文件名。")
                continue

            try:
                data = load_chat(filename)
                backend = data["backend"]
                current_system_prompt = data["system_prompt"]
                messages = data["messages"]
                client = build_client(backend)
                current_session_filename = filename if filename.endswith(".json") else filename + ".json"
                print(f"已加载会话：{current_session_filename}")
                print(f"当前后端：{backend}")
            except Exception as e:
                print(f"加载失败：{e}")
            continue

        if user_input == "/save" or user_input.startswith("/save "):
            filename = user_input[len("/save "):].strip() if user_input.startswith("/save ") else current_session_filename

            try:
                saved_path = save_chat(
                    messages=messages,
                    backend=backend,
                    system_prompt=current_system_prompt,
                    filename=filename
                )
                if filename is None:
                    current_session_filename = saved_path.split("\\")[-1].split("/")[-1]
                else:
                    current_session_filename = filename if filename.endswith(".json") else filename + ".json"
                print(f"会话已保存到：{saved_path}")
            except Exception as e:
                print(f"保存失败：{e}")
            continue

        if user_input.startswith("/rename "):
            new_filename = user_input[len("/rename "):].strip()
            if not new_filename:
                print("请输入新的文件名。")
                continue

            if current_session_filename is None:
                print("当前会话还没有保存过，请先使用 /save。")
                continue

            try:
                new_path = rename_chat(current_session_filename, new_filename)
                current_session_filename = new_filename if new_filename.endswith(".json") else new_filename + ".json"
                print(f"会话已重命名为：{current_session_filename}")
                print(f"新路径：{new_path}")
            except Exception as e:
                print(f"重命名失败：{e}")
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