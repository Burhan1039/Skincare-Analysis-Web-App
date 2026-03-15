# Skin AI Backend (FastAPI + SQLite)

## Run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET /health`
- `POST /api/analyze` (multipart form data)
- `GET /api/analysis/{analysis_id}`
