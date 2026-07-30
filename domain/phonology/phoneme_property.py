from __future__ import annotations

"""
SanskritAI
==========

Phoneme Property

Defines immutable phonological properties that characterize
individual Sanskrit phonemes.

Unlike PhonemeClass, which groups phonemes into traditional
Paninian classes (e.g. Ac, Hal, Antastha), a PhonemeProperty
describes an intrinsic phonetic or articulatory characteristic
of a phoneme.

Version
-------
v1.1.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PhonemeProperty(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable phonological property.
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


# ==========================================================
# Quantity
# ==========================================================

HRASVA = PhonemeProperty(
    "hrasva",
    "Short",
    "ह्रस्व",
    "Short vowel.",
)

DIRGHA = PhonemeProperty(
    "dirgha",
    "Long",
    "दीर्घ",
    "Long vowel.",
)

PLUTA = PhonemeProperty(
    "pluta",
    "Pluta",
    "प्लुत",
    "Prolated vowel.",
)

# ==========================================================
# Place of Articulation
# ==========================================================

KANTHYA = PhonemeProperty(
    "kanthya",
    "Guttural",
    "कण्ठ्य",
)

TALAVYA = PhonemeProperty(
    "talavya",
    "Palatal",
    "तालव्य",
)

MURDHANYA = PhonemeProperty(
    "murdhanya",
    "Retroflex",
    "मूर्धन्य",
)

DANTYA = PhonemeProperty(
    "dantya",
    "Dental",
    "दन्त्य",
)

OSTHYA = PhonemeProperty(
    "osthya",
    "Labial",
    "ओष्ठ्य",
)

# ==========================================================
# Phonation
# ==========================================================

GHOSHA = PhonemeProperty(
    "ghosha",
    "Voiced",
    "घोष",
)

AGHOSHA = PhonemeProperty(
    "aghosha",
    "Voiceless",
    "अघोष",
)

# ==========================================================
# Aspiration
# ==========================================================

ALPAPRANA = PhonemeProperty(
    "alpaprana",
    "Unaspirated",
    "अल्पप्राण",
)

MAHAPRANA = PhonemeProperty(
    "mahaprana",
    "Aspirated",
    "महाप्राण",
)

# ==========================================================
# Nasality
# ==========================================================

NASIKA = PhonemeProperty(
    "nasika",
    "Nasal",
    "नासिक",
)

# ==========================================================
# Miscellaneous / Ayogavaha
# ==========================================================

SEMIVOWEL = PhonemeProperty(
    "semivowel",
    "Semivowel",
    "अन्तःस्थ",
)

SIBILANT = PhonemeProperty(
    "sibilant",
    "Sibilant",
    "ऊष्मन्",
)

AYOGAVAHA = PhonemeProperty(
    "ayogavaha",
    "Ayogavaha",
    "अयोगवाह",
)

JIHVAMULIYA = PhonemeProperty(
    "jihvamuliya",
    "Jihvamuliya",
    "जिह्वामूलीय",
    "Ayogavaha used before gutturals.",
)

UPADHMANIYA = PhonemeProperty(
    "upadhmaniya",
    "Upadhmaniya",
    "उपध्मानीय",
    "Ayogavaha used before labials.",
)
