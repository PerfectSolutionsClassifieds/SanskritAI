from __future__ import annotations

"""
SanskritAI

Anusvāra
"""

from dataclasses import dataclass

from SanskritAI.domain.phonology.non_alphabetic_phoneme import (
    NonAlphabeticPhoneme,
)


@dataclass(frozen=True, slots=True)
class Anusvara(
    NonAlphabeticPhoneme,
):
    """
    Sanskrit Anusvāra (ं)
    """

    @property
    def display_name(self) -> str:
        return "Anusvāra"
