from __future__ import annotations

"""
SanskritAI
==========

Phoneme

Defines the abstract foundation of every Sanskrit phonological
unit.

A Phoneme represents one atomic sound unit independent of any
particular grammatical or lexical interpretation.

Hierarchy
---------

Phoneme
    │
    ├── Vowel
    ├── Consonant
    └── NonAlphabeticPhoneme

Version
-------
v1.0.0
"""

from abc import ABC
from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Phoneme(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Abstract Sanskrit phoneme.
    """

    symbol: str

    transliteration: str = ""

    unicode_name: str = ""

    @property
    def identifier(self) -> str:
        return self.symbol

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.symbol

    @property
    def display_description(self) -> str:
        return self.transliteration

    @property
    def is_vowel(self) -> bool:
        return False

    @property
    def is_consonant(self) -> bool:
        return False

    @property
    def is_non_alphabetic(self) -> bool:
        return False

    def __str__(self) -> str:
        return self.symbol
