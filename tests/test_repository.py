from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from three_high_model.repository import load_sector_evaluations


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


class RepositoryTests(unittest.TestCase):
    def test_loads_csv_snapshot(self) -> None:
        content = (
            "sector_id,name,layer,ranked,growth,profit,moat,valuation,market,confidence,as_of_date\n"
            "sample,示例,上游,true,80,70,90,65,60,85,2026-06-18\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "snapshot.csv"
            path.write_text(content, encoding="utf-8")
            evaluations = load_sector_evaluations(path, WEIGHTS, THRESHOLDS)

        self.assertEqual(len(evaluations), 1)
        self.assertEqual(evaluations[0].sector_id, "sample")
        self.assertTrue(evaluations[0].ranked)


if __name__ == "__main__":
    unittest.main()
