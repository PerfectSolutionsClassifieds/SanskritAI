from __future__ import annotations

"""
SanskritAI
==========

Visarga to S Rule

Concrete visarga Sandhi rule that resolves final visarga to
's' before a suitable following context.

This is a conservative heuristic starter rule and can be
refined later using full phonological conditions.

Version
-------
v1.0.0
"""

from SanskritAI.domain.sandhi.sandhi_context import SandhiContext
from SanskritAI.domain.sandhi.visarga_sandhi_rule import (
    VisargaSandhiRule,
)


class VisargaToSRule(VisargaSandhiRule):
    """
    Heuristic visarga-to-s Sandhi rule.
    """

    @property
    def display_name(self) -> str:
        return "Visarga to S Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic visarga Sandhi rule converting final visarga to s."

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

        return left.endswith("ः")

    def apply(self, context: SandhiContext) -> tuple[str, ...]:
        words = self._extract_words(context)
        if words is None:
            return tuple()

        left, right = words
        if not left.endswith("ः"):
            return tuple()

        transformed = left[:-1] + "स" + right
        return (transformed,)
