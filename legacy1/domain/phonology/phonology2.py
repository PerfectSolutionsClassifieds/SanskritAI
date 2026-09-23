from __future__ import annotations

"""
SanskritAI
==========

Phonology

High-level façade over the canonical Sanskrit phoneme
inventory and phoneme classifier.

Future Sandhi, Morphology, and Grammar kernels should depend
on this façade rather than directly accessing the inventory
or performing phonological checks themselves.

Version
-------
v1.1.0
"""

from SanskritAI.domain.phonology.phoneme import (
    Phoneme,
)
from SanskritAI.domain.phonology.phoneme_classifier import (
    PhonemeClassifier,
)
from SanskritAI.domain.phonology.phoneme_factory import (
    PhonemeFactory,
)
from SanskritAI.domain.phonology.phoneme_inventory import (
    PhonemeInventory,
)


class Phonology:
    """
    Canonical Sanskrit phonology façade.
    """

    def __init__(
        self,
        inventory: PhonemeInventory | None = None,
        classifier: PhonemeClassifier | None = None,
    ) -> None:
        self._inventory = (
            inventory
            if inventory is not None
            else PhonemeFactory.create_default_inventory()
        )
        self._classifier = (
            classifier
            if classifier is not None
            else PhonemeClassifier()
        )

    @property
    def inventory(self) -> PhonemeInventory:
        return self._inventory

    @property
    def classifier(self) -> PhonemeClassifier:
        return self._classifier

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def phoneme(
        self,
        symbol: str,
    ) -> Phoneme | None:
        return self.inventory.get(symbol)

    def contains(
        self,
        symbol: str,
    ) -> bool:
        return self.inventory.contains(symbol)

    # ---------------------------------------------------------
    # Primary Paninian classes
    # ---------------------------------------------------------

    def is_ac(
        self,
        symbol: str,
    ) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_ac(phoneme)

    def is_hal(
        self,
        symbol: str,
    ) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_hal(phoneme)

    def is_ayogavaha(
        self,
        symbol: str,
    ) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_ayogavaha(phoneme)

    # ---------------------------------------------------------
    # Convenience aliases
    # ---------------------------------------------------------

    def is_vowel(
        self,
        symbol: str,
    ) -> bool:
        return self.is_ac(symbol)

    def is_consonant(
        self,
        symbol: str,
    ) -> bool:
        return self.is_hal(symbol)

    def is_non_alphabetic(
        self,
        symbol: str,
    ) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and phoneme.is_non_alphabetic

    def __str__(self) -> str:
        return "Phonology"


DEFAULT_PHONOLOGY = Phonology()
