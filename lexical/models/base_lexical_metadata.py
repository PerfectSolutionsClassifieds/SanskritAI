from __future__ import annotations

"""
SanskritAI
==========

Base Lexical Metadata

Defines the shared immutable metadata contract for lexical
domain objects.

This is the foundation for lexical entities such as:

- LexemeMetadata
- DictionaryEntryMetadata
- DictionarySenseMetadata
- LexicalRelationMetadata

Version
-------
v0.3.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.lexical.enums.lexical_status import LexicalStatus
from SanskritAI.lexical.enums.part_of_speech import PartOfSpeech


@dataclass(frozen=True, slots=True)
class BaseLexicalMetadata:
    """
    Shared lexical metadata.
    """

    lemma: str = ""

    transliteration: str = ""

    language: str = "sanskrit"

    script: str = "devanagari"

    status: LexicalStatus = LexicalStatus.DRAFT

    part_of_speech: PartOfSpeech | None = None

    root: str = ""

    frequency: int = 0

    description: str = ""

    aliases: frozenset[str] = field(
        default_factory=frozenset,
    )

    extra: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def has_lemma(self) -> bool:
        return bool(self.lemma)

    @property
    def has_transliteration(self) -> bool:
        return bool(self.transliteration)

    @property
    def has_root(self) -> bool:
        return bool(self.root)

    @property
    def has_aliases(self) -> bool:
        return bool(self.aliases)

    @property
    def alias_count(self) -> int:
        return len(self.aliases)

    @property
    def is_published(self) -> bool:
        return self.status == LexicalStatus.PUBLISHED

    @property
    def is_verified(self) -> bool:
        return self.status == LexicalStatus.VERIFIED
