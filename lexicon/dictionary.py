from __future__ import annotations

import json
from pathlib import Path

from core.exceptions import DictionaryFormatError


class Dictionary:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.entries = self._load()

    def _load(self) -> dict[str, dict]:
        if not self.path.exists():
            return {}

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return {item["word"]: item for item in data if isinstance(item, dict) and "word" in item}

        if isinstance(data, dict):
            return data

        raise DictionaryFormatError(f"Unsupported dictionary format: {self.path}")

    def lookup(self, word: str) -> dict | None:
        return self.entries.get(word)

    def explain(self, word: str) -> str | None:
        entry = self.lookup(word)
        if not entry:
            return None
        return entry.get("meaning") or entry.get("definition")
