
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Acquisition Result
----------------------------------

Immutable result produced by the Monier-Williams acquisition service
when source content is acquired without parsing.

The result preserves the original source text together with basic
acquisition metadata.

This class belongs to the acquisition layer and intentionally contains
no lexical/domain interpretation.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MonierWilliamsAcquisitionResult:
    """
    Immutable result of acquiring Monier-Williams source content.

    Attributes
    ----------
    text:
        Complete source text exactly as returned by the source.

    source_identifier:
        Stable identifier supplied by the source.

    source_name:
        Human-readable source name.

    character_count:
        Number of characters in the acquired source text.

    line_count:
        Number of logical lines in the acquired source text.
    """

    text: str
    source_identifier: str
    source_name: str
    character_count: int
    line_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")

        if not isinstance(self.source_identifier, str):
            raise TypeError(
                "source_identifier must be a string"
            )

        if not isinstance(self.source_name, str):
            raise TypeError(
                "source_name must be a string"
            )

        if self.character_count < 0:
            raise ValueError(
                "character_count must not be negative"
            )

        if self.line_count < 0:
            raise ValueError(
                "line_count must not be negative"
            )
