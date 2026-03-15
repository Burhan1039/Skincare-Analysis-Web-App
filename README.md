# SkinSense AI (Next.js + FastAPI + SQLite)

An AI-powered skin analysis app for general users.

- Frontend: Next.js (upload Face Photo + questionnaire + personalized results)
- Backend: FastAPI (face detection + skin signal extraction + recommendation engine)
- Database: SQLite (stores analysis history)

## Architecture

- `frontend/` Next.js app for user interaction and results UI
- `backend/` FastAPI API for image analysis and recommendation generation

## 1) Run Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend URL: `http://localhost:8000`

## 2) Run Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Frontend URL: `http://localhost:3000`

## API Contract

### `POST /api/analyze`
Multipart form fields:
- `image` (jpg/png/webp)
- `age_range`
- `lifestyle`
- `primary_concern`
- `sensitivity_level`

Returns:
- inferred skin type
- skin metrics (`dryness_score`, `redness_score`, `oiliness_score`)
- personalized routines and habits
- persisted `analysis_id`

## Notes

- This implementation uses local computer vision heuristics + rule-based recommendations for an MVP.
- Add dermatologist-reviewed logic and/or model APIs before production use.
- App includes a medical disclaimer in results.
