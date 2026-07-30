from __future__ import annotations

"""
SanskritAI
==========

Jihvāmūlīya

Defines the phonological Ayogavāha phoneme used before
guttural consonants in traditional Sanskrit phonology.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.phonology.non_alphabetic_ayogavaha_phoneme import (
    NonAlphabeticAyogavahaPhoneme,
)


@dataclass(frozen=True, slots=True)
class Jihvamuliya(
    NonAlphabeticAyogavahaPhoneme,
):
    """
    Sanskrit Jihvāmūlīya phoneme.
    """

    @property
    def display_name(self) -> str:
        return "Jihvamuliya"

    @property
    def display_text(self) -> str:
        return "ᳵ"

    @property
    def display_description(self) -> str:
        return "Jihvāmūlīya Ayogavāha phoneme."
