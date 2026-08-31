
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalReference:
    """
    Canonical bibliographic / textual reference.
    """

    reference_id: str

    source_name: str

    work: str | None = None
    section: str | None = None
    chapter: str | None = None
    verse: str | None = None
    page: str | None = None
    line: str | None = None
    edition: str | None = None
    publication_year: int | None = None

    url: str | None = None

    citation: str | None = None
    notes: str | None = None

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    @property
    def location(self) -> str:
        parts = [
            self.work,
            self.section,
            self.chapter,
            self.verse,
            self.page,
        ]

        return " : ".join(
            str(part)
            for part in parts
            if part is not None
        )

    def summary(self) -> dict:
        return {
            "source": self.source_name,
            "work": self.work,
            "chapter": self.chapter,
            "verse": self.verse,
            "page": self.page,
        }

    def __str__(self) -> str:
        if self.location:
            return (
                f"{self.source_name} "
                f"({self.location})"
            )

        return self.source_name
