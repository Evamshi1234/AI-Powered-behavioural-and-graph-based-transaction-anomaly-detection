# Deployment Guide

## Local (no Docker)

1. Start backend on port 8000 (see README).
2. Start frontend with `npm run dev` — Vite proxies `/api` to `http://127.0.0.1:8000`.

## Docker — development

```powershell
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| UI | http://localhost:5173 |

Set `VITE_API_PROXY=http://api:8000` in `docker-compose.yml` so the Vite dev server inside Docker can reach the API container.

## Docker — production

```powershell
docker compose -f docker-compose.prod.yml up --build -d
```

| Service | URL |
|---------|-----|
| UI (nginx + static build) | http://localhost |
| API | http://localhost:8000 |

The `web` container proxies `/api` to `api:8000` via nginx. SQLite data persists in the `healthcare_data` volume.

### Environment variables (API)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `demo` | `demo` or `openai` |
| `OPENAI_API_KEY` | — | Required when using OpenAI |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model name |
| `DATABASE_URL` | `sqlite:///./healthcare.db` | Use `sqlite:////data/healthcare.db` in Docker prod |
| `CORS_ORIGINS` | localhost origins | Comma-separated allowed origins |

### Environment variables (UI / nginx)

| Variable | Default | Description |
|----------|---------|-------------|
| `API_UPSTREAM` | `http://api:8000` | Backend base URL for nginx `proxy_pass` |

## Render (Blueprint)

1. Push the repo to GitHub.
2. In Render: **New → Blueprint** and select `render.yaml`.
3. Set `OPENAI_API_KEY` and `CORS_ORIGINS` (your UI URL) on the API service if using OpenAI.
4. The UI service receives `API_UPSTREAM` from the API hostname; the entrypoint adds `https://` when needed.

## Build frontend only (static)

```powershell
cd frontend
npm install
npm run build
```

Output is in `frontend/dist/`. Serve with any static host; ensure `/api` requests reach the FastAPI backend (reverse proxy or same-origin nginx).

## Health checks

- `GET /api/health` — returns `status`, `llm_provider`, and service name.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| UI shows "Backend unavailable" | Confirm API is running; check Vite proxy (dev) or `API_UPSTREAM` (prod nginx). |
| Empty patient list | Demo profiles seed on first API startup when the database is empty. |
| OpenAI errors | Verify `LLM_PROVIDER=openai` and a valid `OPENAI_API_KEY`. |
