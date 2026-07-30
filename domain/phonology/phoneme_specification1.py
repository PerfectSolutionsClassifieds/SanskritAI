from __future__ import annotations

"""
SanskritAI
==========

Phoneme Specification

Defines declarative phoneme specifications used by the
Phonology Kernel.

The specification contains no construction logic.
It simply describes the canonical Sanskrit phonemes.

Construction is delegated to:

    PhonemeFactory

Storage is delegated to:

    PhonemeInventory

This separation keeps the Sanskrit alphabet as immutable
domain data rather than executable logic.

Future specifications
---------------------

• Classical Sanskrit

• Complete Sanskrit Alphabet

• Vedic Sanskrit

• Telugu Script

• Kannada Script

• Grantha Script

• Roman (IAST)

Version
-------
v1.0.0
"""

from typing import TypeAlias

from SanskritAI.domain.phonology.phoneme import (
    Phoneme,
)

from SanskritAI.domain.phonology.vowel import (
    Vowel,
)

from SanskritAI.domain.phonology.consonant import (
    Consonant,
)

from SanskritAI.domain.phonology.visarga import (
    Visarga,
)

from SanskritAI.domain.phonology.anusvara import (
    Anusvara,
)


# ---------------------------------------------------------
# Type Alias
# ---------------------------------------------------------

#
# (
#     Unicode Symbol,
#     Phoneme Class,
#     Transliteration,
#     Unicode Name,
# )
#

PhonemeSpecification: TypeAlias = tuple[
    str,
    type[Phoneme],
    str,
    str,
]


# ---------------------------------------------------------
# Canonical Sanskrit Specification
# ---------------------------------------------------------

#
# NOTE
# ----
#
# This intentionally contains only a small bootstrap
# subset.
#
# The complete Sanskrit alphabet will be added
# incrementally.
#

CANONICAL_PHONEME_SPECIFICATION: tuple[
    PhonemeSpecification,
    ...
] = (

    # -----------------------------------------------------
    # Vowels
    # -----------------------------------------------------

    (
        "अ",
        Vowel,
        "a",
        "DEVANAGARI LETTER A",
    ),

    (
        "आ",
        Vowel,
        "ā",
        "DEVANAGARI LETTER AA",
    ),

    (
        "इ",
        Vowel,
        "i",
        "DEVANAGARI LETTER I",
    ),

    (
        "ई",
        Vowel,
        "ī",
        "DEVANAGARI LETTER II",
    ),

    (
        "उ",
        Vowel,
        "u",
        "DEVANAGARI LETTER U",
    ),

    (
        "ऊ",
        Vowel,
        "ū",
        "DEVANAGARI LETTER UU",
    ),

    # -----------------------------------------------------
    # Consonants
    # -----------------------------------------------------

    (
        "क",
        Consonant,
        "ka",
        "DEVANAGARI LETTER KA",
    ),

    (
        "ख",
        Consonant,
        "kha",
        "DEVANAGARI LETTER KHA",
    ),

    (
        "ग",
        Consonant,
        "ga",
        "DEVANAGARI LETTER GA",
    ),

    # -----------------------------------------------------
    # Ayogavāha
    # -----------------------------------------------------

    (
        "ः",
        Visarga,
        "ḥ",
        "DEVANAGARI SIGN VISARGA",
    ),

    (
        "ं",
        Anusvara,
        "ṃ",
        "DEVANAGARI SIGN ANUSVARA",
    ),

)
