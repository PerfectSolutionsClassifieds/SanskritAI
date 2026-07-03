from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from models.analysis_result import AnalysisResult


class ExporterInterface(ABC):
    @abstractmethod
    def export_json(self, name: str, result: AnalysisResult) -> Path:
        """Export an analysis result and return the output path."""
