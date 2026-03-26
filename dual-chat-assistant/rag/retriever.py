import math

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)

def retrieve_top_k(query_vector, chunk_records, top_k=3):
    scored = []

    for record in chunk_records:
        score = cosine_similarity(query_vector, record["embedding"])
        scored.append(
            {
                "source": record["source"],
                "chunk_id": record["chunk_id"],
                "content": record["content"],
                "score": score,
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]