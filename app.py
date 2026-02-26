from flask import Flask, request, jsonify, send_from_directory
from database.db import get_db_connection
from services.chunking import chunk_text
from services.embeddings import generate_embedding
from services.rag import rag_pipeline
from utils.file_loader import load_pdf
import json
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = load_pdf(path)

    chunks = chunk_text(text)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO documents (filename) VALUES (?)",
                   (file.filename,))
    document_id = cursor.lastrowid

    for chunk in chunks:
        cursor.execute("INSERT INTO chunks (document_id, content) VALUES (?, ?)",
                       (document_id, chunk))
        chunk_id = cursor.lastrowid

        embedding = generate_embedding(chunk)

        cursor.execute("INSERT INTO embeddings (chunk_id, vector) VALUES (?, ?)",
                       (chunk_id, json.dumps(embedding)))

    conn.commit()
    conn.close()

    return jsonify({"message": "Document processed successfully"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = rag_pipeline(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
