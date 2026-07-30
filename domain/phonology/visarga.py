from __future__ import annotations

"""
SanskritAI

Visarga
"""

from dataclasses import dataclass

# from SanskritAI.domain.phonology.non_alphabetic_phoneme import (
#     NonAlphabeticPhoneme,
# )

from SanskritAI.domain.phonology.non_alphabetic_ayogavaha_phoneme import (
    NonAlphabeticAyogavahaPhoneme,
)


@dataclass(frozen=True, slots=True)
class Visarga(
    NonAlphabeticAyogavahaPhoneme,
):
    """
    Sanskrit Visarga (ः)
    """

    @property
    def display_name(self) -> str:
        return "Visarga"
