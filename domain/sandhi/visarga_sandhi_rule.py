from __future__ import annotations

"""
SanskritAI
==========

Visarga Sandhi Rule

Abstract base class for Visarga (ः) Sandhi rules.

Future rules include:

• Visarga → S
• Visarga → R
• Oto R
• Jihvāmūlīya
• Upadhmānīya

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)


class VisargaSandhiRule(
    SandhiRule,
    ABC,
):
    """
    Abstract Visarga Sandhi rule.
    """

    @property
    def display_name(self) -> str:
        return "Visarga Sandhi Rule"

    @property
    def display_description(self) -> str:
        return (
            "Abstract base for all Visarga Sandhi rules."
        )
