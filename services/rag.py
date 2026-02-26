from openai import OpenAI
from config import Config
from services.embeddings import generate_embedding
from services.similarity import search_similar_chunks
from database.db import get_db_connection

client = OpenAI(api_key=Config.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer ONLY using the provided context.
Do not hallucinate.
If the answer is not in context, say:
"I don't have enough information in the knowledge base."
"""

def rag_pipeline(question):
    db_conn = get_db_connection()

    query_embedding = generate_embedding(question)

    top_chunks = search_similar_chunks(query_embedding, db_conn)

    context = "\n\n".join(top_chunks)

    if not context.strip():
        return "I don't have enough information in the knowledge base."

    prompt = f"""
CONTEXT:
{context}

USER QUESTION:
{question}
"""

    response = client.chat.completions.create(
        model=Config.CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content
