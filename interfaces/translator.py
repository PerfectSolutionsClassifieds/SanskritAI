from __future__ import annotations

from abc import ABC, abstractmethod

from models.analysis_result import AnalysisResult


class TranslatorInterface(ABC):
    @abstractmethod
    def translate(self, result: AnalysisResult) -> str:
        """Translate or summarize an analysis result."""
