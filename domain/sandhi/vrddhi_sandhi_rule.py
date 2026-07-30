from __future__ import annotations

"""
SanskritAI
==========

Vrddhi Sandhi Rule

Concrete vowel Sandhi rule for vṛddhi.

This rule performs canonical vowel strengthening when a
vowel boundary triggers vṛddhi formation.

Examples
--------

अ + ए  → ऐ
अ + ऐ  → ऐ
अ + ओ  → औ
अ + औ  → औ

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


class VrddhiSandhiRule(
    SvaraSandhiRule,
):
    """
    Heuristic vṛddhi Sandhi rule.
    """

    _MAPPING: dict[tuple[str, str], str] = {
        ("अ", "ए"): "ऐ",
        ("आ", "ए"): "ऐ",
        ("अ", "ऐ"): "ऐ",
        ("आ", "ऐ"): "ऐ",
        ("अ", "ओ"): "औ",
        ("आ", "ओ"): "औ",
        ("अ", "औ"): "औ",
        ("आ", "औ"): "औ",
    }

    @property
    def display_name(self) -> str:
        return "Vrddhi Sandhi Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic vowel Sandhi rule for vṛddhi."

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
