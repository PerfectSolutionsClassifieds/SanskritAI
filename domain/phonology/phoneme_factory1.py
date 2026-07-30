from __future__ import annotations

"""
SanskritAI
==========

Phoneme Factory

Centralized factory responsible for constructing canonical
Sanskrit phoneme objects.

The factory separates object creation from the inventory,
allowing the inventory to remain a simple immutable registry.

Future extensions
-----------------

• Complete Sanskrit alphabet

• Vedic phonemes

• Script-specific factories

• Custom phonological inventories

Hierarchy
---------

PhonemeFactory
        │
        ├── create_vowel()
        ├── create_consonant()
        ├── create_visarga()
        ├── create_anusvara()
        └── create_default_inventory()

Version
-------
v1.0.0
"""

from SanskritAI.domain.phonology.vowel import Vowel
from SanskritAI.domain.phonology.consonant import Consonant
from SanskritAI.domain.phonology.visarga import Visarga
from SanskritAI.domain.phonology.anusvara import Anusvara
from SanskritAI.domain.phonology.phoneme_inventory import (
    PhonemeInventory,
)


class PhonemeFactory:
    """
    Factory for constructing canonical Sanskrit phonemes.
    """

    # ---------------------------------------------------------
    # Individual Phonemes
    # ---------------------------------------------------------

    @staticmethod
    def create_vowel(
        symbol: str,
        transliteration: str = "",
        unicode_name: str = "",
    ) -> Vowel:

        return Vowel(
            symbol=symbol,
            transliteration=transliteration,
            unicode_name=unicode_name,
        )

    # ---------------------------------------------------------

    @staticmethod
    def create_consonant(
        symbol: str,
        transliteration: str = "",
        unicode_name: str = "",
    ) -> Consonant:

        return Consonant(
            symbol=symbol,
            transliteration=transliteration,
            unicode_name=unicode_name,
        )

    # ---------------------------------------------------------

    @staticmethod
    def create_visarga() -> Visarga:

        return Visarga(
            symbol="ः",
            transliteration="ḥ",
            unicode_name="DEVANAGARI SIGN VISARGA",
        )

    # ---------------------------------------------------------

    @staticmethod
    def create_anusvara() -> Anusvara:

        return Anusvara(
            symbol="ं",
            transliteration="ṃ",
            unicode_name="DEVANAGARI SIGN ANUSVARA",
        )

    # ---------------------------------------------------------
    # Canonical Inventory
    # ---------------------------------------------------------

    @classmethod
    def create_default_inventory(
        cls,
    ) -> PhonemeInventory:
        """
        Constructs the canonical Sanskrit phoneme inventory.

        Initially registers the Ayogavāha phonemes.
        Additional vowels and consonants can be added
        incrementally without changing the inventory API.
        """

        inventory = PhonemeInventory()

        inventory.register(
            cls.create_visarga()
        )

        inventory.register(
            cls.create_anusvara()
        )

        return inventory
