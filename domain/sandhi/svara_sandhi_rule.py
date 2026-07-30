from __future__ import annotations

"""
SanskritAI
==========

Svara Sandhi Rule

Abstract base class for all vowel (स्वर) Sandhi rules.

This family contains Paninian vowel Sandhi transformations,
including:

• Savarṇa Dīrgha
• Guṇa
• Vṛddhi
• Yaṇ
• Ayādi
• Pragṛhya

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)


class SvaraSandhiRule(
    SandhiRule,
    ABC,
):
    """
    Abstract vowel Sandhi rule.
    """

    @property
    def display_name(self) -> str:
        return "Svara Sandhi Rule"

    @property
    def display_description(self) -> str:
        return (
            "Abstract base for all vowel Sandhi rules."
        )
