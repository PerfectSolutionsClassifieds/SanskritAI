
from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalContext:
    """
    Canonical textual context.
    """

    corpus: str

    work: str | None = None
    section: str | None = None
    chapter: str | None = None
    chapter_title: str | None = None
    verse: str | None = None

    page_number: int | None = None
    page_image: str | None = None

    @property
    def identifier(self) -> str:
        parts = [
            self.corpus,
            self.work,
            self.section,
            self.chapter,
            self.verse,
        ]

        return ":".join(
            str(part)
            for part in parts
            if part is not None
        )

    def summary(self) -> dict:
        return {
            "corpus": self.corpus,
            "work": self.work,
            "section": self.section,
            "chapter": self.chapter,
            "verse": self.verse,
        }

    def __str__(self) -> str:
        return (
            f"CanonicalContext("
            f"{self.identifier})"
        )
