from __future__ import annotations

"""
SanskritAI
==========

Dvigu Rule

Concrete heuristic rule for Dvigu compounds.

This rule recognizes compounds with numeral-like first
members, or explicit hints in metadata.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_rule import SamasaRule


class DviguRule(
    SamasaRule,
):
    """
    Heuristic Dvigu compound rule.
    """

    _NUMERAL_PREFIXES: tuple[str, ...] = (
        "एक",
        "द्वि",
        "त्रि",
        "चतुर",
        "पञ्च",
        "षष्",
        "सप्त",
        "अष्ट",
        "नव",
        "दश",
    )

    @property
    def display_name(self) -> str:
        return "Dvigu Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic rule for Dvigu compounds."

    def _extract_text(self, context: SamasaContext) -> str:
        return str(context.subject).strip()

    def _hinted(self, context: SamasaContext) -> bool:
        hint = str(context.get("samasa_hint", "")).lower()
        return hint in {"dvigu", "dvi-gu"}

    def applies_to(self, context: SamasaContext) -> bool:
        text = self._extract_text(context)
        if not text:
            return False

        if self._hinted(context):
            return True

        parts = text.split()
        if len(parts) != 2:
            return False

        left, _ = parts
        return left.startswith(self._NUMERAL_PREFIXES)

    def apply(self, context: SamasaContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = self._extract_text(context)
        left, right = text.split(maxsplit=1)

        return (
            {
                "type": "Dvigu",
                "compound": text,
                "members": (left, right),
                "analysis": f"numeral-head: {left} + {right}",
            },
        )
