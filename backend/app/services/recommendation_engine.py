from __future__ import annotations

from typing import Dict


def infer_skin_type(dryness_score: float, oiliness_score: float, redness_score: float, sensitivity_level: str) -> str:
    if dryness_score > 0.62 and oiliness_score < 0.4:
        base = "Dry"
    elif oiliness_score > 0.62 and dryness_score < 0.45:
        base = "Oily"
    elif 0.45 <= dryness_score <= 0.62 and 0.45 <= oiliness_score <= 0.62:
        base = "Combination"
    else:
        base = "Normal"

    if sensitivity_level.lower() in {"high", "very high"} or redness_score > 0.65:
        return f"{base} + Sensitive"
    return base


def build_recommendations(
    skin_type: str,
    concern: str,
    lifestyle: str,
    sensitivity_level: str,
    metrics: Dict[str, float],
) -> Dict[str, object]:
    cleanser = "Gentle gel cleanser"
    moisturizer = "Ceramide-rich moisturizer"
    sunscreen = "Broad-spectrum SPF 50"
    treatments = []
    habits = []

    lower_type = skin_type.lower()
    lower_concern = concern.lower()

    if "oily" in lower_type:
        cleanser = "Foaming salicylic acid cleanser"
        moisturizer = "Oil-free niacinamide moisturizer"
        treatments.append("2% salicylic acid serum (3x weekly)")
    elif "dry" in lower_type:
        cleanser = "Cream cleanser with glycerin"
        moisturizer = "Barrier-repair cream with ceramides + squalane"
        treatments.append("Hyaluronic acid serum twice daily")
    elif "combination" in lower_type:
        cleanser = "Balanced pH gel cleanser"
        moisturizer = "Lightweight ceramide lotion"
        treatments.append("Niacinamide 5% for T-zone oil control")
    else:
        treatments.append("Niacinamide 5% daily")

    if "sensitive" in lower_type or sensitivity_level.lower() in {"high", "very high"}:
        treatments.append("Azelaic acid 10% every other night")
        habits.append("Patch test all new products for 48 hours")
        habits.append("Avoid fragrance and high alcohol formulations")

    if "acne" in lower_concern or "breakout" in lower_concern:
        treatments.append("Benzoyl peroxide 2.5% spot treatment")
    elif "pigment" in lower_concern or "dark spot" in lower_concern:
        treatments.append("Vitamin C serum in morning")
        treatments.append("Alpha arbutin at night")
    elif "wrinkle" in lower_concern or "aging" in lower_concern:
        treatments.append("Retinol 0.2% at night (start 2x weekly)")
    elif "redness" in lower_concern:
        treatments.append("Centella or panthenol calming serum")

    if lifestyle.lower() in {"outdoor", "active", "sports"}:
        sunscreen = "Water-resistant Broad-spectrum SPF 50+ (reapply every 2h)"
        habits.append("Wear hat/sunglasses for UV protection")

    if metrics.get("dryness_score", 0) > 0.75:
        habits.append("Use humidifier at night and avoid hot showers")
    if metrics.get("oiliness_score", 0) > 0.75:
        habits.append("Blot excess oil during day, avoid over-cleansing")

    morning = [cleanser, "Hydrating serum", moisturizer, sunscreen]
    evening = [cleanser, moisturizer] + treatments[:2]

    return {
        "morning_routine": morning,
        "evening_routine": evening,
        "targeted_treatments": treatments,
        "habits": habits,
        "disclaimer": "This is an AI-assisted wellness recommendation, not a medical diagnosis. Consult a dermatologist for persistent or severe conditions.",
    }
