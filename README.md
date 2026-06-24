# Clinical RAG — Medical Assistant

A minimal Retrieval-Augmented Generation (RAG) demo for clinical documents.

- Backend: FastAPI app that accepts document uploads, ingests text into a vector store, and exposes query/session endpoints.
- Frontend: Vite + React UI for uploading documents and chatting with the assistant.


Key features

- Upload and ingest clinical documents into a per-session vector collection.
- Support for multiple documents: you can upload multiple files (one at a time or in sequence) to the same `session_id`; each uploaded document will be ingested and included in retrievals for that session.
- Local vector store persistence using Chroma (stored under `backend/chroma_store`).


Backend setup

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Create a `.env` file in `backend/` with required variables (example):

```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=sqlite:///./db.sqlite3
CHROMA_PATH=./chroma_store
UPLOAD_DIR=./uploads
```

3. Start the backend (development):

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend setup

1. Install dependencies and start dev server:

```bash
cd frontend
npm install
npm run dev
```

2. Open the dev URL shown by Vite (typically `http://localhost:5173`).



Contribution

- Bug reports and improvements are welcome. Open an issue or submit a PR with tests where appropriate.

