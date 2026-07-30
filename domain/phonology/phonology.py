from __future__ import annotations

"""
SanskritAI
==========

Phonology

High-level façade over the canonical Sanskrit phoneme
inventory and phoneme classifier.

Version
-------
v1.2.0
"""

from SanskritAI.domain.phonology.phoneme import Phoneme
from SanskritAI.domain.phonology.phoneme_classifier import PhonemeClassifier
from SanskritAI.domain.phonology.phoneme_factory import PhonemeFactory
from SanskritAI.domain.phonology.phoneme_inventory import PhonemeInventory


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

    def phoneme(self, symbol: str) -> Phoneme | None:
        return self.inventory.get(symbol)

    def contains(self, symbol: str) -> bool:
        return self.inventory.contains(symbol)

    def is_ac(self, symbol: str) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_ac(phoneme)

    def is_hal(self, symbol: str) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_hal(phoneme)

    def is_ayogavaha(self, symbol: str) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_ayogavaha(phoneme)

    def is_visarga(self, symbol: str) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_visarga(phoneme)

    def is_anusvara(self, symbol: str) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_anusvara(phoneme)

    def is_jihvamuliya(self, symbol: str) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_jihvamuliya(phoneme)

    def is_upadhmaniya(self, symbol: str) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_upadhmaniya(phoneme)

    def is_short_vowel(self, symbol: str) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_short_vowel(phoneme)

    def is_long_vowel(self, symbol: str) -> bool:
        phoneme = self.phoneme(symbol)
        return phoneme is not None and self.classifier.is_long_vowel(phoneme)

    def __str__(self) -> str:
        return "Phonology"


DEFAULT_PHONOLOGY = Phonology()
