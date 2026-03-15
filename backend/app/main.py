from __future__ import annotations

import json

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from app.database import get_session, init_db
from app.models.schemas import AnalysisRecord, AnalysisResponse
from app.services.recommendation_engine import build_recommendations, infer_skin_type
from app.services.skin_analysis import extract_skin_signals

app = FastAPI(title="Skin AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_and_recommend(
    image: UploadFile = File(...),
    age_range: str = Form(...),
    lifestyle: str = Form(...),
    primary_concern: str = Form(...),
    sensitivity_level: str = Form(...),
    session: Session = Depends(get_session),
):
    if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=400, detail="Unsupported image type. Use JPEG/PNG/WEBP")

    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Image is empty")

    try:
        metrics = extract_skin_signals(image_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    skin_type = infer_skin_type(
        dryness_score=metrics["dryness_score"],
        oiliness_score=metrics["oiliness_score"],
        redness_score=metrics["redness_score"],
        sensitivity_level=sensitivity_level,
    )

    recommendations = build_recommendations(
        skin_type=skin_type,
        concern=primary_concern,
        lifestyle=lifestyle,
        sensitivity_level=sensitivity_level,
        metrics=metrics,
    )

    record = AnalysisRecord(
        age_range=age_range,
        lifestyle=lifestyle,
        concern=primary_concern,
        sensitivity_level=sensitivity_level,
        dryness_score=metrics["dryness_score"],
        redness_score=metrics["redness_score"],
        oiliness_score=metrics["oiliness_score"],
        skin_type=skin_type,
        recommendation_json=json.dumps(recommendations),
    )

    session.add(record)
    session.commit()
    session.refresh(record)

    return AnalysisResponse(
        skin_type=skin_type,
        metrics=metrics,
        recommendations=recommendations,
        analysis_id=record.id or -1,
    )


@app.get("/api/analysis/{analysis_id}")
def get_analysis(analysis_id: int, session: Session = Depends(get_session)) -> dict:
    record = session.get(AnalysisRecord, analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": record.id,
        "created_at": record.created_at,
        "skin_type": record.skin_type,
        "metrics": {
            "dryness_score": record.dryness_score,
            "redness_score": record.redness_score,
            "oiliness_score": record.oiliness_score,
        },
        "questionnaire": {
            "age_range": record.age_range,
            "lifestyle": record.lifestyle,
            "primary_concern": record.concern,
            "sensitivity_level": record.sensitivity_level,
        },
        "recommendations": json.loads(record.recommendation_json),
    }
