from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md"}

def load_documents(docs_dir: str = "docs"):
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"文档目录不存在：{docs_dir}")
    
    documents = []

    for file_path in docs_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            content = file_path.read_text(encoding='utf-8')
            documents.append(
                {
                    "source": file_path.name,
                    "content": content,
                }
            )

    return documents