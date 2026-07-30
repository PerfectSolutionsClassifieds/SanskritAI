from __future__ import annotations

"""
SanskritAI
==========

Lemma

Represents the canonical citation form of a Sanskrit
lexeme.

A Lemma is the normalized form under which lexical
knowledge is organized.

Examples
--------

राम

गम्

धर्म

विद्या

Relationship
------------

Lexeme
    │
    └── Lemma
            │
            ├── WordForm
            ├── DictionaryEntry
            └── MorphologicalAnalysis

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Lemma(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable canonical lemma.
    """

    identifier: str

    text: str

    transliteration: str = ""

    language: str = "sanskrit"

    script: str = "devanagari"

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.text

    @property
    def display_text(self) -> str:
        if self.transliteration:
            return f"{self.text} ({self.transliteration})"
        return self.text

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def has_transliteration(self) -> bool:
        return bool(self.transliteration)

    def __str__(self) -> str:
        return self.display_text
