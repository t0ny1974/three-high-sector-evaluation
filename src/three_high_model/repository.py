from __future__ import annotations

import csv
from pathlib import Path

from .model import SectorEvaluation, evaluate_sector


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValueError(f"invalid boolean value: {value}")


def load_sector_evaluations(
    path: Path,
    weights: dict[str, float],
    thresholds: dict[str, float],
) -> list[SectorEvaluation]:
    evaluations: list[SectorEvaluation] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            record: dict[str, object] = dict(row)
            record["ranked"] = _parse_bool(row["ranked"])
            evaluations.append(evaluate_sector(record, weights, thresholds))
    return evaluations
