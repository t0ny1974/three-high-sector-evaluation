from __future__ import annotations

import unittest

import server


class ServerPayloadTests(unittest.TestCase):
    def test_dashboard_payload(self) -> None:
        payload = server.dashboard_payload()
        self.assertEqual(payload["metadata"]["data_kind"], "synthetic-demo")
        self.assertEqual(len(payload["sectors"]), 18)
        self.assertEqual(sum(item["ranked"] for item in payload["sectors"]), 15)


if __name__ == "__main__":
    unittest.main()
