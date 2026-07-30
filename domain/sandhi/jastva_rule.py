from __future__ import annotations

"""
SanskritAI
==========

Jastva Rule

Concrete consonant Sandhi rule for जश्त्व (Jastva).

This rule performs a small heuristic transformation when a
voiced stop or a voiced consonant boundary is encountered.

The implementation is intentionally conservative and can be
expanded later with a full Paninian phonological table.

Version
-------
v1.0.0
"""

from SanskritAI.domain.sandhi.sandhi_context import SandhiContext
from SanskritAI.domain.sandhi.vyanjana_sandhi_rule import (
    VyanjanaSandhiRule,
)


class JastvaRule(VyanjanaSandhiRule):
    """
    Heuristic Jastva Sandhi rule.
    """

    _MAPPING: dict[str, str] = {
        "क": "ग",
        "ख": "घ",
        "च": "ज",
        "छ": "झ",
        "ट": "ड",
        "ठ": "ढ",
        "त": "द",
        "थ": "ध",
        "प": "ब",
        "फ": "भ",
        "स्": "ज",
        "ष्": "ज",
        "श्": "ज",
    }

    @property
    def display_name(self) -> str:
        return "Jastva Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic consonant Sandhi rule for जश्त्व."

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

        return left[-1] in self._MAPPING

    def apply(self, context: SandhiContext) -> tuple[str, ...]:
        words = self._extract_words(context)
        if words is None:
            return tuple()

        left, right = words
        last = left[-1]

        if last not in self._MAPPING:
            return tuple()

        transformed = left[:-1] + self._MAPPING[last] + right
        return (transformed,)
