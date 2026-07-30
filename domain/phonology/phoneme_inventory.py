from __future__ import annotations

"""
SanskritAI
==========

Phoneme Inventory

Defines the immutable canonical repository of Sanskrit
phonemes.

The inventory is intentionally passive. It performs only
lookup operations and never constructs phoneme objects.

Construction is delegated to PhonemeFactory.

Hierarchy
---------

PhonemeFactory
        │
        ▼
PhonemeInventory
        │
        ▼
Phonology

Version
-------
v1.1.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.phonology.phoneme import (
    Phoneme,
)


@dataclass(frozen=True, slots=True)
class PhonemeInventory(
    Immutable,
    Displayable,
):
    """
    Immutable repository of canonical Sanskrit phonemes.
    """

    phonemes: tuple[
        Phoneme,
        ...
    ] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Phoneme Inventory"

    @property
    def display_text(
        self,
    ) -> str:
        return (
            f"{self.count} phonemes"
        )

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Canonical immutable Sanskrit phoneme inventory."
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def count(
        self,
    ) -> int:
        return len(
            self.phonemes
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return self.count == 0

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        symbol: str,
    ) -> Phoneme | None:
        """
        Returns the phoneme corresponding to the supplied
        Unicode symbol.
        """

        for phoneme in self.phonemes:

            if phoneme.symbol == symbol:
                return phoneme

        return None

    # ---------------------------------------------------------

    def contains(
        self,
        symbol: str,
    ) -> bool:
        """
        Determines whether the inventory contains the
        specified phoneme.
        """

        return self.get(
            symbol
        ) is not None

    # ---------------------------------------------------------

    def symbols(
        self,
    ) -> tuple[str, ...]:
        """
        Returns all phoneme symbols.
        """

        return tuple(
            phoneme.symbol
            for phoneme in self.phonemes
        )

    # ---------------------------------------------------------

    def values(
        self,
    ) -> tuple[
        Phoneme,
        ...
    ]:
        """
        Returns every phoneme.
        """

        return self.phonemes

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        return self.count

    # ---------------------------------------------------------

    def __iter__(
        self,
    ):
        return iter(
            self.phonemes
        )

    # ---------------------------------------------------------

    def __contains__(
        self,
        symbol: str,
    ) -> bool:
        return self.contains(
            symbol
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
