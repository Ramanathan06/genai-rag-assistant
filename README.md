# 🧠 GenAI RAG Assistant

> A lightweight **Retrieval-Augmented Generation (RAG)** chatbot that answers questions grounded *only* in your own PDF documents — no hallucinations, no external knowledge.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

---

## ✨ Overview

Upload a PDF, and the assistant turns it into a searchable knowledge base. Ask a question and it retrieves the most relevant passages, feeds them to an LLM as context, and returns an answer **strictly limited to what's in your documents**. If the answer isn't in the knowledge base, it says so instead of making something up.

The whole pipeline is intentionally dependency-light — Flask, the OpenAI SDK, NumPy, and SQLite — so it's easy to read end-to-end and a good reference implementation for understanding how RAG actually works under the hood.

## 🚀 Features

- 📄 **PDF ingestion** — extracts text with `pypdf` and stores it for retrieval
- ✂️ **Overlapping chunking** — splits text into 500-character chunks with 100-character overlap to preserve context across boundaries
- 🔢 **Embeddings** — generates vectors with OpenAI `text-embedding-3-small`
- 🔍 **Semantic search** — cosine-similarity retrieval of the top-k most relevant chunks
- 💬 **Grounded answers** — `gpt-4o-mini` answers using retrieved context only (`temperature=0`), with an explicit anti-hallucination system prompt
- 🗄️ **Persistent store** — documents, chunks, and embeddings persisted in SQLite
- 🌐 **Simple web UI** — upload + chat from the browser, served straight from Flask

## 🏗️ How It Works

```
                          ┌──────────────────────── INGESTION ────────────────────────┐
   PDF upload  ──▶  pypdf text extraction  ──▶  chunk (500 / 100 overlap)  ──▶  OpenAI embeddings
                                                                                      │
                                                                                      ▼
                                                                          SQLite (documents · chunks · embeddings)
                          ┌──────────────────────── RETRIEVAL ────────────────────────┐
   User question  ──▶  embed question  ──▶  cosine similarity vs. all chunks  ──▶  top-3 chunks
                                                                                      │
                                                                                      ▼
                                                       context + question  ──▶  gpt-4o-mini  ──▶  grounded answer
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python · Flask |
| LLM & Embeddings | OpenAI (`gpt-4o-mini`, `text-embedding-3-small`) |
| Vector math | NumPy (cosine similarity) |
| Storage | SQLite |
| PDF parsing | pypdf |
| Frontend | HTML · JavaScript (vanilla) |

## 📁 Project Structure

```
genai-rag-assistant/
├── app.py                  # Flask app + routes (/, /upload, /chat)
├── config.py               # Env config: API key, DB name, model names
├── requirements.txt
├── database/
│   ├── db.py               # SQLite connection helper
│   └── schema.sql          # documents / chunks / embeddings tables
├── services/
│   ├── chunking.py         # Overlapping text chunker
│   ├── embeddings.py       # OpenAI embedding generation
│   ├── similarity.py       # Cosine similarity + top-k retrieval
│   └── rag.py              # End-to-end RAG pipeline
├── utils/
│   └── file_loader.py      # PDF text extraction
├── static/
│   ├── index.html          # Web UI
│   └── app.js
└── uploads/                # Uploaded PDFs land here
```

## ⚡ Getting Started

### Prerequisites
- Python 3.9+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone & install

```bash
git clone https://github.com/Ramanathan06/genai-rag-assistant.git
cd genai-rag-assistant
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure your API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
```

### 3. Initialize the database

The app expects the SQLite schema to exist before first run:

```bash
sqlite3 rag.db < database/schema.sql
```

### 4. Run

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser, upload a PDF, and start asking questions.

## 🔌 API Reference

The web UI is backed by three routes:

| Method | Endpoint | Body | Description |
|---|---|---|---|
| `GET`  | `/`       | — | Serves the chat UI |
| `POST` | `/upload` | `multipart/form-data` with a `file` field | Ingests a PDF: extract → chunk → embed → store |
| `POST` | `/chat`   | `{ "question": "..." }` | Runs the RAG pipeline, returns `{ "answer": "..." }` |

**Example:**

```bash
# Ingest a document
curl -F "file=@handbook.pdf" http://127.0.0.1:5000/upload

# Ask a question
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the refund policy?"}'
```

## ⚙️ Configuration

Models and storage are centralized in `config.py`:

```python
DATABASE        = "rag.db"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL      = "gpt-4o-mini"
```

Swap in larger models (e.g. `gpt-4o`, `text-embedding-3-large`) as needed.

## 📝 Notes & Limitations

This is a focused, educational RAG implementation. A few deliberate simplifications worth knowing:

- **PDF only** — ingestion uses `pypdf`; other formats aren't parsed yet.
- **Brute-force retrieval** — similarity is computed in Python over *all* stored chunks on every query. Great for clarity and small corpora; for large datasets a vector index (FAISS, pgvector, Chroma) would scale far better.
- **Fixed-size chunking** — character-based windows, not sentence- or token-aware.

## 🌱 Possible Improvements

- Plug in a real vector database for sub-linear retrieval
- Support more file types (DOCX, TXT, Markdown, HTML)
- Token-aware / semantic chunking
- Source citations in answers (show which chunks were used)
- Streaming responses and conversation memory

---

<sub>Built by [Ramanathan M](https://github.com/Ramanathan06) · AI / Data Science Engineer</sub>
