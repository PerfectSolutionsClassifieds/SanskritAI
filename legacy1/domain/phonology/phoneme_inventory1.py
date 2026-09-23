from __future__ import annotations

"""
SanskritAI
==========

Phoneme Inventory

Canonical immutable inventory of Sanskrit phonemes.

Provides lookup by Unicode symbol.

Version
-------
v1.0.0
"""

from SanskritAI.domain.phonology.vowel import Vowel
from SanskritAI.domain.phonology.consonant import Consonant
from SanskritAI.domain.phonology.visarga import Visarga
from SanskritAI.domain.phonology.anusvara import Anusvara
from SanskritAI.domain.phonology.phoneme import Phoneme


class PhonemeInventory:
    """
    Canonical Sanskrit phoneme inventory.
    """

    def __init__(self) -> None:

        self._inventory: dict[str, Phoneme] = {}

    # ---------------------------------------------------------

    def register(
        self,
        phoneme: Phoneme,
    ) -> None:

        self._inventory[
            phoneme.symbol
        ] = phoneme

    # ---------------------------------------------------------

    def get(
        self,
        symbol: str,
    ) -> Phoneme | None:

        return self._inventory.get(symbol)

    # ---------------------------------------------------------

    def contains(
        self,
        symbol: str,
    ) -> bool:

        return symbol in self._inventory

    # ---------------------------------------------------------

    def values(
        self,
    ):

        return tuple(
            self._inventory.values()
        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self._inventory)


# ---------------------------------------------------------
# Canonical Inventory
# ---------------------------------------------------------

DEFAULT_PHONEME_INVENTORY = PhonemeInventory()

# Initial phonemes.
DEFAULT_PHONEME_INVENTORY.register(
    Visarga("ः", "ḥ")
)

DEFAULT_PHONEME_INVENTORY.register(
    Anusvara("ं", "ṃ")
)
