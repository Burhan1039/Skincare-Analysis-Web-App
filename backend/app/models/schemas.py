from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class AnalysisRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    age_range: str
    lifestyle: str
    concern: str
    sensitivity_level: str

    dryness_score: float
    redness_score: float
    oiliness_score: float
    skin_type: str

    recommendation_json: str


class QuestionnaireInput(SQLModel):
    age_range: str
    lifestyle: str
    primary_concern: str
    sensitivity_level: str


class AnalysisResponse(SQLModel):
    skin_type: str
    metrics: dict
    recommendations: dict
    analysis_id: int
