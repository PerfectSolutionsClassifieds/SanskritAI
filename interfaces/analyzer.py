from __future__ import annotations

from abc import ABC, abstractmethod

from models.word import Word


class AnalyzerInterface(ABC):
    @abstractmethod
    def analyze(self, tokens: list[str]) -> list[Word]:
        """Analyze tokens into word objects."""
