from __future__ import annotations

import json
from pathlib import Path


class JsonStorage:
    def __init__(self, output_dir: str | Path = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, data: dict) -> Path:
        path = self.output_dir / f"{name}.json"
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return path
