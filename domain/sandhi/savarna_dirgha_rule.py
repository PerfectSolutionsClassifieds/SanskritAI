from __future__ import annotations

"""
SanskritAI
==========

Savarna Dirgha Rule

Concrete vowel Sandhi rule for savarṇa dīrgha.

This rule performs the canonical long-vowel coalescence when
two adjacent vowels of the same class meet at a sandhi
boundary.

Examples
--------

अ + अ  → आ
इ + इ  → ई
उ + उ  → ऊ

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.sandhi.svara_sandhi_rule import (
    SvaraSandhiRule,
)
from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)


class SavarnaDirghaRule(
    SvaraSandhiRule,
):
    """
    Heuristic savarṇa dīrgha Sandhi rule.
    """

    _MAPPING: dict[tuple[str, str], str] = {
        ("अ", "अ"): "आ",
        ("आ", "अ"): "आ",
        ("अ", "आ"): "आ",
        ("आ", "आ"): "आ",
        ("इ", "इ"): "ई",
        ("ई", "ई"): "ई",
        ("इ", "ई"): "ई",
        ("ई", "इ"): "ई",
        ("उ", "उ"): "ऊ",
        ("ऊ", "ऊ"): "ऊ",
        ("उ", "ऊ"): "ऊ",
        ("ऊ", "उ"): "ऊ",
    }

    @property
    def display_name(self) -> str:
        return "Savarna Dirgha Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic vowel Sandhi rule for savarṇa dīrgha."

    def _extract_words(self, context: SandhiContext) -> tuple[str, str] | None:
        text = str(context.subject).strip()
        if not text:
            return None

        parts = text.split()
        if len(parts) != 2:
            return None

        return parts[0], parts[1]

    def applies_to(self, context: SandhiContext) -> bool:
        words = self._extract_words(context)
        if words is None:
            return False

        left, right = words
        if not left or not right:
            return False

        return (left[-1], right[0]) in self._MAPPING

    def apply(self, context: SandhiContext) -> tuple[str, ...]:
        words = self._extract_words(context)
        if words is None:
            return tuple()

        left, right = words
        key = (left[-1], right[0])

        if key not in self._MAPPING:
            return tuple()

        transformed = left[:-1] + self._MAPPING[key] + right[1:]
        return (transformed,)
