def split_text(text: str, chunk_size: int = 200, chunk_overlap: int = 50):
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap 不能小于 0")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap 必须小于 chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def split_documents(documents, chunk_size: int = 200, chunk_overlap: int = 50):
    all_chunks = []

    for doc in documents:
        source = doc["source"]
        content = doc["content"]

        chunks = split_text(
            text=content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for idx, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "source": source,
                    "chunk_id": idx,
                    "content": chunk,
                }
            )

    return all_chunks