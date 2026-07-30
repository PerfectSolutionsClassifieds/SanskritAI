from __future__ import annotations

"""
SanskritAI
==========

Guna Sandhi Rule

Concrete vowel Sandhi rule for guṇa.

This rule performs the canonical vowel strengthening when a
short/long a-vowel meets i/ī or u/ū at a sandhi boundary.

Examples
--------

अ + इ  → ए
अ + ई  → ए
अ + उ  → ओ
अ + ऊ  → ओ

Version
-------
v1.0.0
"""

from SanskritAI.domain.sandhi.svara_sandhi_rule import (
    SvaraSandhiRule,
)
from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)


class GunaSandhiRule(
    SvaraSandhiRule,
):
    """
    Heuristic guṇa Sandhi rule.
    """

    _MAPPING: dict[tuple[str, str], str] = {
        ("अ", "इ"): "ए",
        ("अ", "ई"): "ए",
        ("आ", "इ"): "ए",
        ("आ", "ई"): "ए",
        ("अ", "उ"): "ओ",
        ("अ", "ऊ"): "ओ",
        ("आ", "उ"): "ओ",
        ("आ", "ऊ"): "ओ",
        ("अ", "ऋ"): "अर्",
        ("आ", "ऋ"): "अर्",
    }

    @property
    def display_name(self) -> str:
        return "Guna Sandhi Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic vowel Sandhi rule for guṇa."

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
