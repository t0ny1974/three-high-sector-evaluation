from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ModelSettings:
    model_version: str
    investment_horizon: str
    quality_weights: dict[str, float]
    status_thresholds: dict[str, float]
    display: dict[str, float]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_model_settings(path: Path) -> ModelSettings:
    payload = load_json(path)
    weights = {name: float(value) for name, value in payload["quality_weights"].items()}
    if set(weights) != {"growth", "profit", "moat"}:
        raise ValueError("quality_weights must contain growth, profit and moat")
    if any(weight < 0 for weight in weights.values()):
        raise ValueError("quality_weights cannot contain negative values")
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("quality_weights must sum to 1.0")

    return ModelSettings(
        model_version=str(payload["model_version"]),
        investment_horizon=str(payload["investment_horizon"]),
        quality_weights=weights,
        status_thresholds={
            name: float(value) for name, value in payload["status_thresholds"].items()
        },
        display={name: float(value) for name, value in payload["display"].items()},
    )
