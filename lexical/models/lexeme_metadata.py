from __future__ import annotations

"""
SanskritAI
==========

Lexeme Metadata

Defines the immutable metadata for a Lexeme.

A LexemeMetadata object captures the canonical lexical
information for a lemma-independent lexical unit.

It builds upon BaseLexicalMetadata and adds lexeme-specific
semantic fields only when needed.

Version
-------
v0.3.0
"""

from dataclasses import dataclass

from SanskritAI.lexical.enums.lexical_status import LexicalStatus
from SanskritAI.lexical.enums.part_of_speech import PartOfSpeech
from SanskritAI.lexical.models.base_lexical_metadata import (
    BaseLexicalMetadata,
)


@dataclass(frozen=True, slots=True)
class LexemeMetadata(BaseLexicalMetadata):
    """
    Immutable metadata describing a Lexeme.
    """

    title: str = ""

    @property
    def display_title(self) -> str:
        """
        Preferred human-readable title for the lexeme.
        Falls back to lemma when title is not provided.
        """
        if self.title:
            return self.title
        return self.lemma

    @property
    def has_title(self) -> bool:
        return bool(self.title)

    @property
    def canonical_name(self) -> str:
        """
        Canonical lexical name.
        """
        return self.lemma

    @property
    def is_known(self) -> bool:
        """
        Indicates whether the lexeme has a canonical lemma.
        """
        return self.has_lemma

    @classmethod
    def from_lemma(
        cls,
        lemma: str,
        *,
        transliteration: str = "",
        language: str = "sanskrit",
        script: str = "devanagari",
        status: LexicalStatus = LexicalStatus.DRAFT,
        part_of_speech: PartOfSpeech | None = None,
        root: str = "",
        frequency: int = 0,
        description: str = "",
    ) -> "LexemeMetadata":
        """
        Convenience constructor for building a lexeme metadata
        object from a lemma.
        """
        return cls(
            lemma=lemma,
            transliteration=transliteration,
            language=language,
            script=script,
            status=status,
            part_of_speech=part_of_speech,
            root=root,
            frequency=frequency,
            description=description,
            title=lemma,
        )
