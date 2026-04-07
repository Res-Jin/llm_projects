from pathlib import Path
from rag.pdf_loader import load_pdf_text


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def load_text_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    return {
        "source": file_path.name,
        "content": content,
    }


def load_documents(docs_dir: str = "docs"):
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"文档目录不存在：{docs_dir}")

    documents = []

    for file_path in docs_path.iterdir():
        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()

        if suffix not in SUPPORTED_EXTENSIONS:
            continue

        if suffix in {".txt", ".md"}:
            doc = load_text_file(file_path)
            documents.append(doc)

        elif suffix == ".pdf":
            doc = load_pdf_text(str(file_path))
            documents.append(doc)

    return documents