from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Acquisition Service
------------------------------------

Coordinates:

    Source
      |
      v
    Parser
      |
      v
    MonierWilliamsRecord

The service intentionally does not know anything about
the canonical lexical repository.
"""

from dataclasses import dataclass

from SanskritAI.domain.lexical.adapters.monier_williams_record import (
    MonierWilliamsRecord,
)

from .monier_williams_parser import MonierWilliamsParser
from .monier_williams_source import MonierWilliamsSource


@dataclass(frozen=True, slots=True)
class MonierWilliamsAcquisitionService:
    """
    Coordinates source reading and parsing.
    """

    source: MonierWilliamsSource
    parser: MonierWilliamsParser

    def acquire(self) -> tuple[MonierWilliamsRecord, ...]:
        """
        Acquire and parse the configured source.
        """
        source_text = self.source.read()

        return self.parser.parse(
            source_text,
        )

    def count(self) -> int:
        """
        Return the number of parsed records.
        """
        return len(self.acquire())
