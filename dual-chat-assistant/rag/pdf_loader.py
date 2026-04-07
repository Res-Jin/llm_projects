from pathlib import Path
from pypdf import PdfReader


def load_pdf_text(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF 文件不存在：{file_path}")

    reader = PdfReader(str(path))
    pages = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = text.strip()

        if text:
            pages.append(
                {
                    "page": page_num + 1,
                    "text": text,
                }
            )

    full_text = "\n\n".join(page["text"] for page in pages)

    return {
        "source": path.name,
        "content": full_text,
        "pages": pages,
    }