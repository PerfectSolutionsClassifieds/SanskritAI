from __future__ import annotations

"""
SanskritAI
==========

Lexeme

Defines the immutable canonical lexical unit in the Sanskrit
Domain Layer.

A Lexeme represents the underlying dictionary-level word unit
independent of any particular inflected form. It is the
foundation for the Lexical Kernel.

Architecture
------------

Lexeme
    │
    ├── Lemma
    ├── WordForm
    ├── DictionaryEntry
    └── DictionarySense

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Lexeme(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable canonical lexical unit.

    This class is intentionally lightweight and semantic.
    It does not encode dictionary-specific senses, grammar
    analysis, or morphological transformations.
    """

    identifier: str

    lemma: str

    language: str = "sanskrit"

    script: str = "devanagari"

    transliteration: str = ""

    description: str = ""

    aliases: frozenset[str] = field(
        default_factory=frozenset,
    )

    @property
    def display_name(self) -> str:
        return self.lemma

    @property
    def display_text(self) -> str:
        if self.transliteration:
            return f"{self.lemma} ({self.transliteration})"
        return self.lemma

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def alias_count(self) -> int:
        return len(self.aliases)

    @property
    def has_aliases(self) -> bool:
        return bool(self.aliases)

    @property
    def has_transliteration(self) -> bool:
        return bool(self.transliteration)

    def matches(
        self,
        text: str,
    ) -> bool:
        """
        Determines whether the supplied text matches the lexeme
        identifier, lemma, transliteration, or aliases.
        """
        normalized = text.strip()
        if not normalized:
            return False

        return (
            normalized == self.identifier
            or normalized == self.lemma
            or normalized == self.transliteration
            or normalized in self.aliases
        )

    def __str__(self) -> str:
        return self.display_text
