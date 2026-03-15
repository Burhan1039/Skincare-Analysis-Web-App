# Skin AI Frontend (Next.js)

## Run

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open: http://localhost:3000

## Backend Connectivity

Frontend uses a same-origin Next.js API proxy at `/api/analyze`.

Set backend target in `.env.local`:

```bash
BACKEND_URL=http://127.0.0.1:8000
```

This avoids browser-side CORS/network issues from direct cross-origin calls.
