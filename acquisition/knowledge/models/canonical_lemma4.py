
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalLemma:
    """
    Canonical lexical lemma.
    """

    lemma: str

    transliteration: str | None = None

    language: str = "sa"
    script: str = "Devanagari"

    dhatu: str | None = None
    part_of_speech: str | None = None
    lexical_category: str | None = None

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    def summary(self) -> dict:
        return {
            "lemma": self.lemma,
            "dhatu": self.dhatu,
            "part_of_speech": self.part_of_speech,
            "category": self.lexical_category,
        }

    @property
    def display_name(self) -> str:
        return self.lemma

    def __str__(self) -> str:
        return (
            "CanonicalLemma("
            f"{self.lemma})"
        )
