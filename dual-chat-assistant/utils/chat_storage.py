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

    if not filename.endswith(".json"):
        filename += ".json"

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

def list_chat_sessions():
    files = sorted(CHAT_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [f.name for f in files]

def load_chat(filename):
    if not filename.endswith(".json"):
        filename += ".json"

    file_path = CHAT_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"会话文件不存在：{filename}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

def rename_chat(old_filename, new_filename):
    if not old_filename.endswith(".json"):
        old_filename += ".json"
    if not new_filename.endswith(".json"):
        new_filename += ".json"

    old_path = CHAT_DIR / old_filename
    new_path = CHAT_DIR / new_filename

    if not old_path.exists():
        raise FileNotFoundError(f"原会话文件不存在：{old_filename}")

    if new_path.exists():
        raise FileExistsError(f"目标文件已存在：{new_filename}")

    old_path.rename(new_path)
    return str(new_path)

def get_session_display_list():
    files = list_chat_sessions()
    return files