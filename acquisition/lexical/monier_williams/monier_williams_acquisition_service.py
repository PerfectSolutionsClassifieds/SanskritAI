from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .monier_williams_parser import MonierWilliamsParser
from .monier_williams_source import MonierWilliamsSource


@dataclass(frozen=True, slots=True)
class MonierWilliamsAcquisitionService:
    """Coordinates source acquisition and parsing."""

    source: MonierWilliamsSource
    parser: MonierWilliamsParser | None = None

    def read(self) -> str:
        return self.source.read()

    def acquire(self):
        source_text = self.source.read()

        if self.parser is None:
            return source_text

        return self.parser.parse(source_text)

    def count(self) -> int:
        result = self.acquire()

        if isinstance(result, str):
            return len(result.splitlines()) if result else 0

        return len(result)
