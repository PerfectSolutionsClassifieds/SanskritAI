from __future__ import annotations

"""
SanskritAI
==========

Phoneme Factory

Constructs immutable Sanskrit phoneme inventories from a
declarative specification.

The factory is the sole component responsible for creating
canonical phoneme objects. PhonemeInventory remains an
immutable repository and never constructs phonemes itself.

Future
------

• Classical Sanskrit Inventory

• Vedic Inventory

• Telugu Script Inventory

• Kannada Script Inventory

• Grantha Script Inventory

Version
-------
v1.1.0
"""

from typing import Type

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

from SanskritAI.domain.phonology.phoneme_inventory import (
    PhonemeInventory,
)


# ---------------------------------------------------------
# Canonical Sanskrit Phoneme Specification
# ---------------------------------------------------------

#
# Format
#
# (
#     Unicode Symbol,
#     Phoneme Class,
#     Transliteration,
#     Unicode Name,
# )
#

PHONEME_SPECIFICATION: tuple[
    tuple[
        str,
        Type[Phoneme],
        str,
        str,
    ],
    ...
] = (

    # -----------------------------------------------------
    # Vowels (initial subset)
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
    # Consonants (initial subset)
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


class PhonemeFactory:
    """
    Factory responsible for constructing immutable Sanskrit
    phoneme inventories.
    """

    # -----------------------------------------------------

    @staticmethod
    def create_phoneme(
        symbol: str,
        phoneme_type: Type[Phoneme],
        transliteration: str = "",
        unicode_name: str = "",
    ) -> Phoneme:
        """
        Constructs a single phoneme.
        """

        return phoneme_type(
            symbol=symbol,
            transliteration=transliteration,
            unicode_name=unicode_name,
        )

    # -----------------------------------------------------

    @classmethod
    def create_inventory(
        cls,
        specification=PHONEME_SPECIFICATION,
    ) -> PhonemeInventory:
        """
        Builds a phoneme inventory from a declarative
        specification.
        """

        phonemes = tuple(

            cls.create_phoneme(

                symbol=symbol,

                phoneme_type=phoneme_type,

                transliteration=transliteration,

                unicode_name=unicode_name,

            )

            for (
                symbol,
                phoneme_type,
                transliteration,
                unicode_name,
            )

            in specification

        )

        return PhonemeInventory(

            phonemes=phonemes,

        )

    # -----------------------------------------------------

    @classmethod
    def create_default_inventory(
        cls,
    ) -> PhonemeInventory:
        """
        Returns the canonical Sanskrit phoneme inventory.
        """

        return cls.create_inventory()
