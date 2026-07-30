from __future__ import annotations

"""
SanskritAI

Visarga
"""

from dataclasses import dataclass

from SanskritAI.domain.phonology.non_alphabetic_phoneme import (
    NonAlphabeticPhoneme,
)


@dataclass(frozen=True, slots=True)
class Visarga(
    NonAlphabeticPhoneme,
):
    """
    Sanskrit Visarga (ः)
    """

    @property
    def display_name(self) -> str:
        return "Visarga"
