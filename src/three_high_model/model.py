from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping


SCORE_NAMES = ("growth", "profit", "moat", "valuation", "market", "confidence")


@dataclass(frozen=True)
class SectorEvaluation:
    sector_id: str
    name: str
    layer: str
    ranked: bool
    growth: float
    profit: float
    moat: float
    valuation: float
    market: float
    confidence: float
    quality: float
    status: str
    as_of_date: str


def _validate_score(name: str, value: float) -> float:
    score = float(value)
    if not math.isfinite(score) or not 0 <= score <= 100:
        raise ValueError(f"{name} must be a finite number between 0 and 100")
    return score


def quality_score(
    growth: float,
    profit: float,
    moat: float,
    weights: Mapping[str, float],
) -> float:
    values = {
        "growth": _validate_score("growth", growth),
        "profit": _validate_score("profit", profit),
        "moat": _validate_score("moat", moat),
    }
    if set(weights) != set(values):
        raise ValueError("weights must contain growth, profit and moat")
    if any(float(weight) < 0 for weight in weights.values()):
        raise ValueError("weights cannot contain negative values")
    if abs(sum(float(weight) for weight in weights.values()) - 1.0) > 1e-9:
        raise ValueError("weights must sum to 1.0")
    return round(sum(values[name] * float(weights[name]) for name in values), 2)


def research_status(
    *,
    ranked: bool,
    quality: float,
    valuation: float,
    market: float,
    confidence: float,
    thresholds: Mapping[str, float],
) -> str:
    quality = _validate_score("quality", quality)
    valuation = _validate_score("valuation", valuation)
    market = _validate_score("market", market)
    confidence = _validate_score("confidence", confidence)

    if not ranked:
        return "观察板块"
    if confidence < thresholds["minimum_confidence"]:
        return "数据不足"
    if quality >= thresholds["high_quality"]:
        if valuation > thresholds["expensive"]:
            return "质量优秀，等待估值"
        if market < thresholds["market_weak"]:
            return "质量优秀，趋势未确认"
        if market >= thresholds["market_confirmed"]:
            return "重点研究"
        return "质量优秀，等待确认"
    if quality >= thresholds["normal_quality"]:
        return "普通观察"
    return "暂不关注"


def evaluate_sector(
    record: Mapping[str, object],
    weights: Mapping[str, float],
    thresholds: Mapping[str, float],
) -> SectorEvaluation:
    scores = {name: _validate_score(name, float(record[name])) for name in SCORE_NAMES}
    quality = quality_score(scores["growth"], scores["profit"], scores["moat"], weights)
    ranked = bool(record["ranked"])
    status = research_status(
        ranked=ranked,
        quality=quality,
        valuation=scores["valuation"],
        market=scores["market"],
        confidence=scores["confidence"],
        thresholds=thresholds,
    )
    return SectorEvaluation(
        sector_id=str(record["sector_id"]),
        name=str(record["name"]),
        layer=str(record["layer"]),
        ranked=ranked,
        growth=scores["growth"],
        profit=scores["profit"],
        moat=scores["moat"],
        valuation=scores["valuation"],
        market=scores["market"],
        confidence=scores["confidence"],
        quality=quality,
        status=status,
        as_of_date=str(record["as_of_date"]),
    )
