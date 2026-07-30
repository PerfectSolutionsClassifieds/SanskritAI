from __future__ import annotations

"""
SanskritAI
==========

Phoneme Specification

Defines immutable declarative phoneme specifications used by
the Phonology Kernel.

Version
-------
v2.1.0
"""

from typing import TypeAlias

from SanskritAI.domain.phonology.anusvara import Anusvara
from SanskritAI.domain.phonology.consonant import Consonant
from SanskritAI.domain.phonology.jihvamuliya import Jihvamuliya
from SanskritAI.domain.phonology.phoneme import Phoneme
from SanskritAI.domain.phonology.upadhmaniya import Upadhmaniya
from SanskritAI.domain.phonology.visarga import Visarga
from SanskritAI.domain.phonology.vowel import Vowel
from SanskritAI.domain.phonology.phoneme_property import (
    AC,
    AGHOSHA,
    ALPAPRANA,
    AYOGAVAHA,
    DIRGHA,
    GHOSHA,
    HRASVA,
    JIHVAMULIYA,
    KANTHYA,
    MAHAPRANA,
    OSTHYA,
    UPADHMANIYA,
)


PhonemeSpecification: TypeAlias = tuple[
    str,
    type[Phoneme],
    str,
    str,
    tuple,
]


CANONICAL_PHONEME_SPECIFICATION: tuple[
    PhonemeSpecification,
    ...
] = (
    (
        "अ",
        Vowel,
        "a",
        "DEVANAGARI LETTER A",
        (HRASVA, KANTHYA),
    ),
    (
        "आ",
        Vowel,
        "ā",
        "DEVANAGARI LETTER AA",
        (DIRGHA, KANTHYA),
    ),
    (
        "इ",
        Vowel,
        "i",
        "DEVANAGARI LETTER I",
        (HRASVA, KANTHYA),
    ),
    (
        "ई",
        Vowel,
        "ī",
        "DEVANAGARI LETTER II",
        (DIRGHA, KANTHYA),
    ),
    (
        "उ",
        Vowel,
        "u",
        "DEVANAGARI LETTER U",
        (HRASVA, OSTHYA),
    ),
    (
        "ऊ",
        Vowel,
        "ū",
        "DEVANAGARI LETTER UU",
        (DIRGHA, OSTHYA),
    ),
    (
        "क",
        Consonant,
        "ka",
        "DEVANAGARI LETTER KA",
        (AGHOSHA, ALPAPRANA, KANTHYA),
    ),
    (
        "ख",
        Consonant,
        "kha",
        "DEVANAGARI LETTER KHA",
        (AGHOSHA, MAHAPRANA, KANTHYA),
    ),
    (
        "ग",
        Consonant,
        "ga",
        "DEVANAGARI LETTER GA",
        (GHOSHA, ALPAPRANA, KANTHYA),
    ),
    (
        "ः",
        Visarga,
        "ḥ",
        "DEVANAGARI SIGN VISARGA",
        (AYOGAVAHA,),
    ),
    (
        "ं",
        Anusvara,
        "ṃ",
        "DEVANAGARI SIGN ANUSVARA",
        (AYOGAVAHA,),
    ),
    (
        "ᳵ",
        Jihvamuliya,
        "jihvamuliya",
        "DEVANAGARI SIGN JIHVAMULIYA",
        (AYOGAVAHA, JIHVAMULIYA),
    ),
    (
        "ᳶ",
        Upadhmaniya,
        "upadhmaniya",
        "DEVANAGARI SIGN UPADHMANIYA",
        (AYOGAVAHA, UPADHMANIYA),
    ),
)
