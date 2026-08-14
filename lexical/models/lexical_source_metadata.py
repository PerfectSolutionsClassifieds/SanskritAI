from __future__ import annotations
from dataclasses import dataclass
from SanskritAI.lexical.models.base_lexical_metadata import BaseLexicalMetadata

@dataclass(frozen=True, slots=True)
class LexicalSourceMetadata(BaseLexicalMetadata):
    """
    Metadata describing a lexical source.
    """
    description: str | None = None
    language: str | None = None
    script: str | None = None
    edition: str | None = None
    publisher: str | None = None
    year: int | None = None
