import numpy as np
import json

def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def search_similar_chunks(query_embedding, db_conn, top_k=3):
    cursor = db_conn.cursor()
    cursor.execute("""
        SELECT chunks.content, embeddings.vector
        FROM embeddings
        JOIN chunks ON embeddings.chunk_id = chunks.id
    """)

    results = []
    for row in cursor.fetchall():
        vector = json.loads(row["vector"])
        score = cosine_similarity(query_embedding, vector)
        results.append((row["content"], score))

    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results[:top_k]]
