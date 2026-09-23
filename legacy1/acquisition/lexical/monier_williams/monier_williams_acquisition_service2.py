
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Acquisition Service
------------------------------------

Owns the source boundary but does not parse or canonicalize
the acquired material.
"""

from dataclasses import dataclass

from .monier_williams_source import MonierWilliamsSource


@dataclass(frozen=True, slots=True)
class MonierWilliamsAcquisitionResult:
    """
    Result of source acquisition.
    """

    source: str
    text: str

    @property
    def character_count(self) -> int:
        return len(self.text)

    @property
    def line_count(self) -> int:
        if not self.text:
            return 0
        return len(self.text.splitlines())


class MonierWilliamsAcquisitionService:
    """
    Acquire raw Monier-Williams source material.
    """

    def __init__(self, source: MonierWilliamsSource) -> None:
        if not isinstance(source, MonierWilliamsSource):
            raise TypeError(
                "source must implement MonierWilliamsSource"
            )

        self.source = source

    def acquire(self) -> str:
        return self.source.acquire()

    def read(self) -> str:
        return self.acquire()

    def acquire_result(self) -> MonierWilliamsAcquisitionResult:
        text = self.acquire()

        return MonierWilliamsAcquisitionResult(
            source=self.source.identifier,
            text=text,
        )

    def count_lines(self) -> int:
        return self.acquire_result().line_count
