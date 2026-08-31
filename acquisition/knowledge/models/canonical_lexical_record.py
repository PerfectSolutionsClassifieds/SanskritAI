
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalLexicalRecord:
    """
    Canonical lexical record shared by every lexical
    acquisition pipeline.
    """

    headword: str

    transliteration: str | None = None

    language: str = "sa"
    script: str = "Devanagari"

    definition: str = ""

    entry_type: str | None = None

    source_name: str = ""
    source_version: str = ""
    source_record_id: str = ""

    citation: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def summary(self) -> dict:
        return {
            "headword": self.headword,
            "source": self.source_name,
            "version": self.source_version,
            "entry_type": self.entry_type,
        }

    def __str__(self) -> str:
        return (
            f"CanonicalLexicalRecord("
            f"{self.headword})"
        )
