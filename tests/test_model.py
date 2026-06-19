from __future__ import annotations

import unittest

from three_high_model.model import evaluate_sector, quality_score, research_status


WEIGHTS = {"growth": 0.35, "profit": 0.30, "moat": 0.35}
THRESHOLDS = {
    "high_quality": 70,
    "normal_quality": 55,
    "expensive": 70,
    "extremely_expensive": 85,
    "market_confirmed": 55,
    "market_weak": 45,
    "minimum_confidence": 60,
}


class QualityScoreTests(unittest.TestCase):
    def test_weighted_quality_score(self) -> None:
        self.assertEqual(quality_score(80, 70, 90, WEIGHTS), 80.5)

    def test_rejects_out_of_range_score(self) -> None:
        with self.assertRaisesRegex(ValueError, "growth"):
            quality_score(101, 70, 90, WEIGHTS)

    def test_rejects_invalid_weights(self) -> None:
        with self.assertRaisesRegex(ValueError, "sum"):
            quality_score(80, 70, 90, {"growth": 0.5, "profit": 0.5, "moat": 0.5})

    def test_rejects_negative_weights(self) -> None:
        with self.assertRaisesRegex(ValueError, "negative"):
            quality_score(80, 70, 90, {"growth": 0.8, "profit": 0.3, "moat": -0.1})


class ResearchStatusTests(unittest.TestCase):
    def test_low_confidence_takes_priority(self) -> None:
        status = research_status(
            ranked=True,
            quality=85,
            valuation=50,
            market=80,
            confidence=59,
            thresholds=THRESHOLDS,
        )
        self.assertEqual(status, "数据不足")

    def test_observation_sector_is_not_ranked(self) -> None:
        status = research_status(
            ranked=False,
            quality=85,
            valuation=50,
            market=80,
            confidence=90,
            thresholds=THRESHOLDS,
        )
        self.assertEqual(status, "观察板块")

    def test_high_quality_confirmed_sector(self) -> None:
        status = research_status(
            ranked=True,
            quality=75,
            valuation=65,
            market=60,
            confidence=80,
            thresholds=THRESHOLDS,
        )
        self.assertEqual(status, "重点研究")

    def test_expensive_sector_waits_for_valuation(self) -> None:
        status = research_status(
            ranked=True,
            quality=75,
            valuation=71,
            market=70,
            confidence=80,
            thresholds=THRESHOLDS,
        )
        self.assertEqual(status, "质量优秀，等待估值")


class EvaluationTests(unittest.TestCase):
    def test_evaluation_contains_traceable_result(self) -> None:
        result = evaluate_sector(
            {
                "sector_id": "example",
                "name": "示例板块",
                "layer": "上游",
                "ranked": True,
                "growth": 80,
                "profit": 70,
                "moat": 90,
                "valuation": 65,
                "market": 60,
                "confidence": 85,
                "as_of_date": "2026-06-18",
            },
            WEIGHTS,
            THRESHOLDS,
        )
        self.assertEqual(result.quality, 80.5)
        self.assertEqual(result.status, "重点研究")
        self.assertEqual(result.as_of_date, "2026-06-18")


if __name__ == "__main__":
    unittest.main()
