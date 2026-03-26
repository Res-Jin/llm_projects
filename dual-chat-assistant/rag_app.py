from rag.document_loader import load_documents
from rag.text_splitter import split_documents
from rag.embedding_client import OllamaEmbeddingClient
from rag.retriever import retrieve_top_k
from rag.rag_pipeline import generate_rag_answer


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
    print("=== Local Knowledge QA - Step 3 ===")

    try:
        backend = choose_backend()

        documents = load_documents("docs")
        print(f"\n已加载文档数：{len(documents)}")

        chunks = split_documents(
            documents,
            chunk_size=80,
            chunk_overlap=20
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
                    "chunk_id": chunk["chunk_id"],
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
            top_chunks = retrieve_top_k(query_vector, chunk_records, top_k=3)

            print("\n最相关的文本块：")
            for idx, item in enumerate(top_chunks, start=1):
                print(f"\n[Top {idx}]")
                print(f"source: {item['source']}")
                print(f"chunk_id: {item['chunk_id']}")
                print(f"score: {item['score']:.4f}")
                print("content:")
                print(item["content"])
                print("-" * 50)

            answer = generate_rag_answer(query, top_chunks, backend=backend)

            print("\n回答：")
            print(answer)

            print("\n参考来源：")
            for item in top_chunks:
                print(f"- {item['source']} chunk {item['chunk_id']}")

            print("\n" + "=" * 60 + "\n")

    except Exception as e:
        print(f"运行失败：{e}")


if __name__ == "__main__":
    main()