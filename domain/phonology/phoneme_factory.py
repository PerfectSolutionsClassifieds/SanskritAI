from __future__ import annotations

"""
SanskritAI
==========

Phoneme Factory

Constructs immutable phoneme inventories from declarative
phoneme specifications.

The factory contains no hard-coded Sanskrit alphabet.
Canonical Sanskrit phonemes are defined separately in
phoneme_specification.py.

Hierarchy
---------

Phoneme Specification
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

The same factory can construct:

• Classical Sanskrit inventory

• Complete Sanskrit inventory

• Vedic inventory

• Telugu script inventory

• Kannada script inventory

• Grantha script inventory

Version
-------
v1.3.0
"""

from collections.abc import Iterable

from SanskritAI.domain.phonology.phoneme import (
    Phoneme,
)

from SanskritAI.domain.phonology.phoneme_inventory import (
    PhonemeInventory,
)

from SanskritAI.domain.phonology.phoneme_specification import (
    CANONICAL_PHONEME_SPECIFICATION,
    PhonemeSpecification,
)


class PhonemeFactory:
    """
    Factory responsible for constructing immutable phoneme
    inventories from declarative specifications.
    """

    # ---------------------------------------------------------
    # Individual Phoneme
    # ---------------------------------------------------------

    @staticmethod
    def create_phoneme(
        specification: PhonemeSpecification,
    ) -> Phoneme:
        """
        Constructs a single phoneme from a declarative
        specification.
        """

        (
            symbol,
            phoneme_type,
            transliteration,
            unicode_name,
            properties,
        ) = specification

        return phoneme_type(
            symbol=symbol,
            transliteration=transliteration,
            unicode_name=unicode_name,
            properties=properties,
        )

    # ---------------------------------------------------------
    # Multiple Phonemes
    # ---------------------------------------------------------

    @classmethod
    def create_phonemes(
        cls,
        specification: Iterable[PhonemeSpecification],
    ) -> tuple[Phoneme, ...]:
        """
        Constructs immutable phonemes from a specification.
        """

        return tuple(
            cls.create_phoneme(item)
            for item in specification
        )

    # ---------------------------------------------------------
    # Inventory
    # ---------------------------------------------------------

    @classmethod
    def create_inventory(
        cls,
        specification: Iterable[PhonemeSpecification],
    ) -> PhonemeInventory:
        """
        Constructs an immutable phoneme inventory.
        """

        return PhonemeInventory(
            phonemes=cls.create_phonemes(
                specification
            )
        )

    # ---------------------------------------------------------
    # Canonical Sanskrit Inventory
    # ---------------------------------------------------------

    @classmethod
    def create_default_inventory(
        cls,
    ) -> PhonemeInventory:
        """
        Constructs the canonical Sanskrit phoneme inventory.
        """

        return cls.create_inventory(
            CANONICAL_PHONEME_SPECIFICATION
        )
