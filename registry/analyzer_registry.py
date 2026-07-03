from __future__ import annotations

from interfaces.analyzer import AnalyzerInterface


class AnalyzerRegistry:
    def __init__(self):
        self._analyzers: dict[str, AnalyzerInterface] = {}

    def register(self, name: str, analyzer: AnalyzerInterface) -> None:
        self._analyzers[name] = analyzer

    def get(self, name: str) -> AnalyzerInterface | None:
        return self._analyzers.get(name)

    def names(self) -> list[str]:
        return sorted(self._analyzers)
