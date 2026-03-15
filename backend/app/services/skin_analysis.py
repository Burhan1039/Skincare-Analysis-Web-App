from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import cv2
import numpy as np


@dataclass
class SkinSignals:
    dryness_score: float
    redness_score: float
    oiliness_score: float


def _safe_crop_face(image_bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(90, 90))

    if len(faces) == 0:
        h, w = image_bgr.shape[:2]
        top, bottom = int(h * 0.15), int(h * 0.85)
        left, right = int(w * 0.2), int(w * 0.8)
        return image_bgr[top:bottom, left:right]

    x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
    pad = int(0.15 * max(w, h))
    y1, y2 = max(0, y - pad), min(image_bgr.shape[0], y + h + pad)
    x1, x2 = max(0, x - pad), min(image_bgr.shape[1], x + w + pad)
    return image_bgr[y1:y2, x1:x2]


def _normalize(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.5
    clipped = max(low, min(high, value))
    return float((clipped - low) / (high - low))


def extract_skin_signals(image_bytes: bytes) -> Dict[str, float]:
    arr = np.frombuffer(image_bytes, np.uint8)
    image_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("Could not decode image data")

    face = _safe_crop_face(image_bgr)
    face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face_hsv = cv2.cvtColor(face, cv2.COLOR_BGR2HSV)

    red_channel = face_rgb[:, :, 0].astype(np.float32)
    green_channel = face_rgb[:, :, 1].astype(np.float32)
    blue_channel = face_rgb[:, :, 2].astype(np.float32)
    value_channel = face_hsv[:, :, 2].astype(np.float32)

    dryness_raw = float(np.std(value_channel) / 64.0)
    redness_raw = float(np.mean(red_channel - (green_channel + blue_channel) / 2.0))
    oiliness_raw = float(np.mean(value_channel) / 255.0)

    dryness_score = _normalize(dryness_raw, 0.08, 0.75)
    redness_score = _normalize(redness_raw, -5.0, 45.0)
    oiliness_score = _normalize(oiliness_raw, 0.2, 0.9)

    return {
        "dryness_score": round(dryness_score, 3),
        "redness_score": round(redness_score, 3),
        "oiliness_score": round(oiliness_score, 3),
    }
