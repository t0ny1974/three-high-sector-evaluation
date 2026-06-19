from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
WEB_ROOT = ROOT / "web"
sys.path.insert(0, str(ROOT / "src"))

from three_high_model.config import load_model_settings  # noqa: E402
from three_high_model.repository import load_sector_evaluations  # noqa: E402


def dashboard_payload() -> dict[str, object]:
    settings = load_model_settings(ROOT / "config" / "model.json")
    evaluations = load_sector_evaluations(
        ROOT / "data" / "sample" / "sector_scores.csv",
        settings.quality_weights,
        settings.status_thresholds,
    )
    return {
        "metadata": {
            "model_version": settings.model_version,
            "investment_horizon": settings.investment_horizon,
            "data_kind": "synthetic-demo",
            "disclaimer": "合成演示数据，不构成投资建议。",
        },
        "sectors": [asdict(item) for item in evaluations],
    }


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def _send_json(self, payload: object, status: int = 200) -> None:
        content = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json({"status": "ok"})
            return
        if path == "/api/sectors":
            self._send_json(dashboard_payload())
            return
        super().do_GET()

    def log_message(self, format: str, *args: object) -> None:
        print(f"[dashboard] {self.address_string()} - {format % args}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the three-high sector dashboard.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8501, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"三高产业链板块评估模型：http://{args.host}:{args.port}")
    print("按 Ctrl+C 停止服务器。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
