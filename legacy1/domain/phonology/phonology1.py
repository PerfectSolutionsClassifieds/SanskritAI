from __future__ import annotations

"""
SanskritAI
==========

Phonology

High-level façade over the canonical Sanskrit phoneme
inventory.

Future Sandhi, Morphology and Grammar kernels should depend
on this façade rather than directly accessing the inventory.

Version
-------
v1.0.0
"""

from SanskritAI.domain.phonology.phoneme import (
    Phoneme,
)

from SanskritAI.domain.phonology.phoneme_inventory import (
    DEFAULT_PHONEME_INVENTORY,
)


class Phonology:
    """
    Canonical Sanskrit phonology façade.
    """

    def __init__(self):

        self._inventory = DEFAULT_PHONEME_INVENTORY

    @property
    def inventory(self):

        return self._inventory

    # ---------------------------------------------------------

    def phoneme(
        self,
        symbol: str,
    ) -> Phoneme | None:

        return self.inventory.get(symbol)

    # ---------------------------------------------------------

    def contains(
        self,
        symbol: str,
    ) -> bool:

        return self.inventory.contains(symbol)

    # ---------------------------------------------------------

    def is_vowel(
        self,
        symbol: str,
    ) -> bool:

        phoneme = self.phoneme(symbol)

        return (
            phoneme is not None
            and phoneme.is_vowel
        )

    # ---------------------------------------------------------

    def is_consonant(
        self,
        symbol: str,
    ) -> bool:

        phoneme = self.phoneme(symbol)

        return (
            phoneme is not None
            and phoneme.is_consonant
        )

    # ---------------------------------------------------------

    def is_ayogavaha(
        self,
        symbol: str,
    ) -> bool:

        phoneme = self.phoneme(symbol)

        return (
            phoneme is not None
            and getattr(
                phoneme,
                "is_ayogavaha",
                False,
            )
        )


DEFAULT_PHONOLOGY = Phonology()
