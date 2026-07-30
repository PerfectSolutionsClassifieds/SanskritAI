from __future__ import annotations

"""
SanskritAI
==========

Phoneme Specification

Defines immutable declarative phoneme specifications used by
the Phonology Kernel.

The specification contains no construction logic.

Each specification completely describes one phoneme.

Hierarchy
---------

PhonemeSpecification
        │
        ▼
PhonemeFactory
        │
        ▼
PhonemeInventory
        │
        ▼
Phonology

Future
------

• Complete Sanskrit Alphabet

• Vedic Inventory

• Telugu Script Inventory

• Kannada Script Inventory

• Grantha Script Inventory

Version
-------
v2.0.0
"""

from typing import TypeAlias

from SanskritAI.domain.phonology.phoneme import Phoneme
from SanskritAI.domain.phonology.vowel import Vowel
from SanskritAI.domain.phonology.consonant import Consonant
from SanskritAI.domain.phonology.visarga import Visarga
from SanskritAI.domain.phonology.anusvara import Anusvara

from SanskritAI.domain.phonology.phoneme_property import (
    HRASVA,
    DIRGHA,
    KANTHYA,
    AYOGAVAHA,
)


# ---------------------------------------------------------
# Type Alias
# ---------------------------------------------------------

#
# (
#     Unicode Symbol,
#     Phoneme Type,
#     Transliteration,
#     Unicode Name,
#     Phonological Properties,
# )
#

PhonemeSpecification: TypeAlias = tuple[
    str,
    type[Phoneme],
    str,
    str,
    tuple,
]


# ---------------------------------------------------------
# Canonical Bootstrap Specification
# ---------------------------------------------------------

CANONICAL_PHONEME_SPECIFICATION: tuple[
    PhonemeSpecification,
    ...
] = (

    # =====================================================
    # Vowels
    # =====================================================

    (
        "अ",
        Vowel,
        "a",
        "DEVANAGARI LETTER A",
        (
            HRASVA,
            KANTHYA,
        ),
    ),

    (
        "आ",
        Vowel,
        "ā",
        "DEVANAGARI LETTER AA",
        (
            DIRGHA,
            KANTHYA,
        ),
    ),

    (
        "इ",
        Vowel,
        "i",
        "DEVANAGARI LETTER I",
        (
            HRASVA,
        ),
    ),

    (
        "ई",
        Vowel,
        "ī",
        "DEVANAGARI LETTER II",
        (
            DIRGHA,
        ),
    ),

    (
        "उ",
        Vowel,
        "u",
        "DEVANAGARI LETTER U",
        (
            HRASVA,
        ),
    ),

    (
        "ऊ",
        Vowel,
        "ū",
        "DEVANAGARI LETTER UU",
        (
            DIRGHA,
        ),
    ),

    # =====================================================
    # Consonants
    # =====================================================

    (
        "क",
        Consonant,
        "ka",
        "DEVANAGARI LETTER KA",
        (
            KANTHYA,
        ),
    ),

    (
        "ख",
        Consonant,
        "kha",
        "DEVANAGARI LETTER KHA",
        (
            KANTHYA,
        ),
    ),

    (
        "ग",
        Consonant,
        "ga",
        "DEVANAGARI LETTER GA",
        (
            KANTHYA,
        ),
    ),

    # =====================================================
    # Ayogavāha
    # =====================================================

    (
        "ः",
        Visarga,
        "ḥ",
        "DEVANAGARI SIGN VISARGA",
        (
            AYOGAVAHA,
        ),
    ),

    (
        "ं",
        Anusvara,
        "ṃ",
        "DEVANAGARI SIGN ANUSVARA",
        (
            AYOGAVAHA,
        ),
    ),

)
