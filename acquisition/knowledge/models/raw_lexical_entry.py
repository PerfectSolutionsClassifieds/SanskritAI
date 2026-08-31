
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class RawLexicalEntry:
    """
    Immutable lexical record extracted directly from
    an external resource.
    """

    source_name: str
    source_version: str
    source_record_id: str

    source_url: str | None = None
    citation: str | None = None
    license: str | None = None

    headword: str = ""
    raw_text: str = ""

    language: str = "sa"
    script: str = "Devanagari"

    transliteration: str | None = None
    entry_type: str | None = None
    section: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def has_headword(self) -> bool:
        return bool(
            self.headword.strip(),
        )

    @property
    def has_raw_text(self) -> bool:
        return bool(
            self.raw_text.strip(),
        )

    def summary(self) -> dict:
        return {
            "source": self.source_name,
            "record_id": self.source_record_id,
            "headword": self.headword,
            "script": self.script,
            "language": self.language,
            "entry_type": self.entry_type,
        }

    def __str__(self) -> str:
        return (
            "RawLexicalEntry("
            f"{self.source_name}: "
            f"{self.headword})"
        )
