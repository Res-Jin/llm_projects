import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent #BASE_DIR指向项目根目录
CHAT_DIR = BASE_DIR / "chats"
CHAT_DIR.mkdir(exist_ok=True)

def generate_chat_filename() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"chat_{timestamp}.json"

def save_chat(messages, backend, system_prompt, filename=None):
    if filename is None:
        filename = generate_chat_filename()

    file_path = CHAT_DIR / filename

    data = {
        "backend": backend,
        "system_prompt": system_prompt,
        "messages": messages,
        "saved_at": datetime.now().isoformat(timespec="seconds")
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return str(file_path)