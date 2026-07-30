from __future__ import annotations

"""
SanskritAI
==========

Vyanjana Sandhi Rule

Abstract base class for consonant (व्यञ्जन) Sandhi rules.

Future rules include:

• Jastva
• Chatva
• Parasavarṇa
• Tugāgama
• Anunāsika
• Lopa

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)


class VyanjanaSandhiRule(
    SandhiRule,
    ABC,
):
    """
    Abstract consonant Sandhi rule.
    """

    @property
    def display_name(self) -> str:
        return "Vyanjana Sandhi Rule"

    @property
    def display_description(self) -> str:
        return (
            "Abstract base for all consonant Sandhi rules."
        )
