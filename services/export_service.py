from __future__ import annotations

from pathlib import Path

from models.analysis_result import AnalysisResult
from storage.json_storage import JsonStorage


class ExportService:
    def __init__(self, storage: JsonStorage | None = None):
        self.storage = storage or JsonStorage()

    def export_json(self, name: str, result: AnalysisResult) -> Path:
        return self.storage.save(name, result.to_dict())
