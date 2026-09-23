# Personalized Healthcare Assistant with Generative AI

End-to-end full-stack project: profile-aware health chat, retrieval-augmented generation (RAG), safety guardrails, and optional OpenAI integration.

## Features

| Layer | Capability |
|-------|------------|
| **Frontend** | React + Vite + Tailwind — patient profiles, multi-conversation chat |
| **Backend** | FastAPI + SQLite — REST API, conversation history |
| **Generative AI** | OpenAI (`gpt-4o-mini`) or built-in **demo mode** (no API key) |
| **RAG** | Keyword retrieval over curated wellness knowledge base |
| **Safety** | Emergency phrase detection, medical disclaimers, no diagnosis |

## Architecture

```
Browser (React) ──► FastAPI ──► SQLite
                      │
                      ├── RAG (knowledge_base.json)
                      ├── Safety checks
                      └── LLM (demo | OpenAI)
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## Quick start (local)

### 1. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

API docs: http://127.0.0.1:8000/docs

### 2. Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open: http://localhost:5173

### 3. Enable OpenAI (optional)

Edit `backend/.env`:

```env
OPENAI_API_KEY=sk-your-key
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
```

## Docker (development)

```powershell
docker compose up --build
```

- API: http://localhost:8000  
- UI: http://localhost:5173 (Vite proxies `/api` to the backend)

## Docker (production)

```powershell
docker compose -f docker-compose.prod.yml up --build
```

- UI + API proxy: http://localhost (port 80)  
- API direct: http://localhost:8000  

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for Render and other hosting options.

## API overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Service status |
| GET/POST | `/api/profiles` | List / create patients |
| PUT/DELETE | `/api/profiles/{id}` | Update / delete |
| POST | `/api/chat` | Send message (creates conversation if needed) |
| GET | `/api/chat/conversations/{profile_id}` | List chats |
| GET | `/api/chat/messages/{conversation_id}` | Message history |

### Example chat request

```json
{
  "profile_id": 1,
  "message": "How can I manage blood pressure with diet?"
}
```

## Project structure

```
personalized-healthcare-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   └── services/   # llm, rag, safety
│   └── requirements.txt
├── frontend/
│   └── src/
├── docs/
└── docker-compose.yml
```

## Disclaimer

This project is for **education and demonstration**. It does not provide medical diagnosis or treatment. Always consult qualified healthcare professionals for clinical decisions.

## License

MIT — use freely for learning and portfolio projects.
