from rag.document_loader import load_documents
from rag.text_splitter import split_documents
from rag.embedding_client import OllamaEmbeddingClient
from rag.retriever import retrieve_top_k, filter_by_score
from rag.rag_pipeline import generate_rag_answer
from config import (
    RAG_DOCS_DIR,
    RAG_CHUNK_SIZE,
    RAG_CHUNK_OVERLAP,
    RAG_TOP_K,
    RAG_MIN_SCORE,
)

def merge_sources_for_display(chunks):
    if not chunks:
        return []

    sorted_chunks = sorted(
        chunks,
        key=lambda x: (
            x["source"],
            -1 if x.get("page") is None else x["page"],
            x["chunk_id"],
        )
    )

    merged = []
    current = None

    for item in sorted_chunks:
        source = item["source"]
        page = item.get("page")
        chunk_id = item["chunk_id"]
        score = item["score"]

        if current is None:
            current = {
                "source": source,
                "page": page,
                "start_chunk_id": chunk_id,
                "end_chunk_id": chunk_id,
                "scores": [score],
            }
            continue

        same_source = current["source"] == source
        same_page = current["page"] == page
        adjacent_chunk = chunk_id == current["end_chunk_id"] + 1

        if same_source and same_page and adjacent_chunk:
            current["end_chunk_id"] = chunk_id
            current["scores"].append(score)
        else:
            merged.append(current)
            current = {
                "source": source,
                "page": page,
                "start_chunk_id": chunk_id,
                "end_chunk_id": chunk_id,
                "scores": [score],
            }

    if current is not None:
        merged.append(current)

    return merged

def choose_backend():
    while True:
        print("\n请选择回答模型后端：")
        print("1. Qwen API")
        print("2. Ollama Local")
        choice = input("输入 1 或 2：").strip()

        if choice == "1":
            return "qwen"
        elif choice == "2":
            return "ollama"
        else:
            print("输入无效，请重新选择。")


def main():
    print("=== Local Knowledge QA - Step 4 ===")

    try:
        backend = choose_backend()

        documents = load_documents(RAG_DOCS_DIR)
        print(f"\n已加载文档数：{len(documents)}")
        print("\n已加载文档列表：")
        for doc in documents:
            print("-", doc["source"])

        chunks = split_documents(
            documents,
            chunk_size=RAG_CHUNK_SIZE,
            chunk_overlap=RAG_CHUNK_OVERLAP
        )
        print(f"已生成文本块数：{len(chunks)}")

        embed_client = OllamaEmbeddingClient()

        chunk_texts = [chunk["content"] for chunk in chunks]
        embeddings = embed_client.embed_texts(chunk_texts)

        chunk_records = []
        for chunk, embedding in zip(chunks, embeddings):
                chunk_records.append(
                {
                    "source": chunk["source"],
                    "page": chunk.get("page"),
                    "chunk_id": chunk["chunk_id"],
                    "page_chunk_id": chunk.get("page_chunk_id"),
                    "content": chunk["content"],
                    "embedding": embedding,
                }
            )

        print("已完成文档块向量化。\n")

        while True:
            query = input("请输入问题（输入 exit 退出）：").strip()
            if query.lower() in {"exit", "quit"}:
                print("程序结束。")
                break

            if not query:
                continue

            query_vector = embed_client.embed_query(query)
            top_chunks = retrieve_top_k(query_vector, chunk_records, top_k=RAG_TOP_K)
            valid_chunks = filter_by_score(top_chunks, RAG_MIN_SCORE)

            if not valid_chunks:
                print("\n回答：")
                print("根据当前提供的资料，无法确定。")
                print("\n提示：没有检索到足够相关的文本块。")
                print("\n" + "=" * 60 + "\n")
                continue

            answer = generate_rag_answer(query, valid_chunks, backend=backend)

            print("\n回答：")
            print(answer)

            print("\n参考来源：")
            merged_sources = merge_sources_for_display(valid_chunks)

            for item in merged_sources:
                avg_score = sum(item["scores"]) / len(item["scores"])
                start_id = item["start_chunk_id"]
                end_id = item["end_chunk_id"]

                if item["page"] is not None:
                    if start_id == end_id:
                        print(
                            f"- {item['source']} page {item['page']} chunk {start_id} "
                            f"(avg_score={avg_score:.4f})"
                        )
                    else:
                        print(
                            f"- {item['source']} page {item['page']} chunks {start_id}-{end_id} "
                            f"(avg_score={avg_score:.4f})"
                        )
                else:
                    if start_id == end_id:
                        print(
                            f"- {item['source']} chunk {start_id} "
                            f"(avg_score={avg_score:.4f})"
                        )
                    else:
                        print(
                            f"- {item['source']} chunks {start_id}-{end_id} "
                            f"(avg_score={avg_score:.4f})"
                        )

            print("\n" + "=" * 60 + "\n")

    except Exception as e:
        print(f"运行失败：{e}")


if __name__ == "__main__":
    main()