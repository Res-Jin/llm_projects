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

        # PDF：按页切块，并保留 page 信息
        if "pages" in doc and doc["pages"]:
            global_chunk_id = 0

            for page_item in doc["pages"]:
                page_num = page_item["page"]
                page_text = page_item["text"]

                page_chunks = split_text(
                    text=page_text,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )

                for local_idx, chunk in enumerate(page_chunks):
                    all_chunks.append(
                        {
                            "source": source,
                            "page": page_num,
                            "chunk_id": global_chunk_id,
                            "page_chunk_id": local_idx,
                            "content": chunk,
                        }
                    )
                    global_chunk_id += 1

        # txt / md：按全文切块
        else:
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
                        "page": None,
                        "chunk_id": idx,
                        "page_chunk_id": None,
                        "content": chunk,
                    }
                )

    return all_chunks