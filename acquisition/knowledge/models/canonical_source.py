
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalSource:
    """
    Canonical description of a lexical or textual source.
    """

    source_id: str

    name: str
    short_name: str | None = None

    source_type: str | None = None

    language: str = "sa"
    script: str | None = None

    author: str | None = None
    editor: str | None = None
    publisher: str | None = None
    edition: str | None = None
    publication_year: int | None = None
    version: str | None = None

    website: str | None = None
    download_url: str | None = None
    api_endpoint: str | None = None
    license: str | None = None

    description: str | None = None
    notes: str | None = None

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    @property
    def display_name(self) -> str:
        return self.short_name or self.name

    @property
    def is_online(self) -> bool:
        return (
            self.website is not None
            or self.download_url is not None
            or self.api_endpoint is not None
        )

    @property
    def is_lexicon(self) -> bool:
        return (
            self.source_type is not None
            and self.source_type.lower() == "lexicon"
        )

    @property
    def is_primary_text(self) -> bool:
        return (
            self.source_type is not None
            and self.source_type.lower() == "primary_text"
        )

    @property
    def is_grammar(self) -> bool:
        return (
            self.source_type is not None
            and self.source_type.lower() == "grammar"
        )

    def summary(self) -> dict:
        return {
            "source_id": self.source_id,
            "name": self.name,
            "type": self.source_type,
            "edition": self.edition,
            "version": self.version,
            "online": self.is_online,
        }

    def __str__(self) -> str:
        return (
            "CanonicalSource("
            f"{self.display_name}"
            ")"
        )
