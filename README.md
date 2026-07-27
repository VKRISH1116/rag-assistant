# 🤖 RAG Assistant

A lightweight full-stack document Q&A app that lets you upload PDFs, TXT files, or DOCX documents and ask questions about them. The current implementation is verified and working end to end in demo mode, with no OpenAI API key required.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![React](https://img.shields.io/badge/React-18.2-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## What is working now

The repository currently supports the following verified workflow:

- Upload a document in PDF, TXT, or DOCX format
- Process the document and split it into searchable chunks
- Ask questions about the uploaded content through the web UI
- View the document list and remove documents from the active index
- Keep a simple conversation history for the current session
- Export a conversation as a text file

This is a working demo-style RAG experience. It uses simple keyword-based retrieval in the current default mode, which makes it easy to run locally without API costs.

## Current status

The app is currently running in demo mode by default unless an OpenAI key is provided.

- Demo mode: works without an API key
- Full mode: present in the codebase, but the verified and easiest path is the demo workflow

## Tech stack

- Backend: FastAPI + Python
- Frontend: React + Axios
- Document parsing: PyPDF2, python-docx
- Text splitting: LangChain text splitters
- Deployment options: Docker and Azure-ready structure

## Project structure

```text
rag-assistant-main/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── rag_engine.py
│   │   ├── rag_engine_demo.py
│   │   ├── agent.py
│   │   └── models.py
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   └── package.json
├── data/
│   └── sample_document.txt
└── docker-compose.yml
```

## Quick start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Optional: OpenAI API key if you want to explore the full-mode path

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 2. Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm start
```

Then open http://localhost:3000.

## Environment variables

### Backend

```env
# Optional, for trying the OpenAI-based path
OPENAI_API_KEY=your-key-here

# Optional, keeps the app in demo mode by default
USE_DEMO_MODE=true
```

### Frontend

```env
REACT_APP_API_URL=http://localhost:8000
```

## Verified features

### Document workflow

- Upload documents through the UI or API
- Store them in the backend upload folder
- Index the content for retrieval
- List and delete uploaded documents

### Q&A workflow

- Ask questions about an uploaded document
- Receive a short answer based on the document content
- See the sources used for the reply

### Conversation tools

- Keep a simple conversation history for a session
- Export the conversation as a text file

## API overview

### Health

```bash
curl http://localhost:8000/health
```

### Upload

```bash
curl -X POST http://localhost:8000/upload -F "file=@document.pdf"
```

### List documents

```bash
curl http://localhost:8000/documents
```

### Delete document

```bash
curl -X DELETE http://localhost:8000/documents/document.pdf
```

### Ask a question

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is this document about?"}'
```

## Current limitations

This project is a solid working demo, but it is not yet a production-grade multi-user system. The current limitations include:

- Simple retrieval rather than a fully optimized vector search pipeline
- No authentication or user accounts
- Conversation history is stored in memory for the current process
- Export is currently a plain text file, not PDF
- The extra agentic workflow is not the primary verified path in the current demo setup

## Docker

From the repo root:

```bash
docker-compose up --build
```

This runs the backend and frontend together.

## Testing

The repository includes a basic regression test for the upload/list/delete flow.

```bash
cd backend
python -m unittest discover -s tests -p 'test_*.py' -v
```

## Contributors

- Yatin

## License

This project is intended for educational and portfolio use.




