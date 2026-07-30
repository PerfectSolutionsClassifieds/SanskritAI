from __future__ import annotations

"""
SanskritAI
==========

Phoneme Class

Defines immutable phonological classes used throughout the
Phonology and Sandhi kernels.

A PhonemeClass represents a traditional Sanskrit phonological
classification (e.g. अच्, हल्, अन्तःस्थ, ऊष्मन्).

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PhonemeClass(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Sanskrit phonological class.
    """

    identifier: str

    name: str

    sanskrit_name: str

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    def __str__(self) -> str:
        return self.display_text


# ---------------------------------------------------------
# Canonical Paninian Classes
# ---------------------------------------------------------

AC = PhonemeClass(
    "ac",
    "Vowel",
    "अच्",
    "All Sanskrit vowels.",
)

HAL = PhonemeClass(
    "hal",
    "Consonant",
    "हल्",
    "All Sanskrit consonants.",
)

ANTASTHA = PhonemeClass(
    "antastha",
    "Semivowel",
    "अन्तःस्थ",
    "य र ल व",
)

USHMAN = PhonemeClass(
    "ushman",
    "Sibilant / Aspirate",
    "ऊष्मन्",
    "श ष स ह",
)

AYOGAVAHA = PhonemeClass(
    "ayogavaha",
    "Ayogavaha",
    "अयोगवाह",
    "Visarga, Anusvāra and related phonetic signs.",
)
