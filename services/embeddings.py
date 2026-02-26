from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_embedding(text):
    response = client.embeddings.create(
        model=Config.EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding
