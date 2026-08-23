
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Record Model

Represents one raw MW dictionary record.

This is intentionally NOT the final DictionaryEntry model.

The MW record contains source-specific structure that must be
preserved until normalization has been completed.
"""

from dataclasses import dataclass, field


@dataclass
class MonierWilliamsRecord:
    """
    One raw Monier-Williams dictionary record.
    """

    line_id: str | None = None

    page: str | None = None

    key1: str | None = None

    key2: str | None = None

    homonym: str | None = None

    entry_number: str | None = None

    body: list[str] = field(default_factory=list)

    raw_text: str = ""

    def add_line(self, line: str) -> None:
        """
        Append one source line to the record.
        """

        self.body.append(line)

    @property
    def text(self) -> str:
        """
        Return the record body as a single string.
        """

        return "\n".join(self.body)
