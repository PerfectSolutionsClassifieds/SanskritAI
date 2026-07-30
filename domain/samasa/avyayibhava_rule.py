from __future__ import annotations

"""
SanskritAI
==========

Avyayibhava Rule

Concrete heuristic rule for Avyayībhāva compounds.

This rule recognizes compounds whose first member behaves as
an indeclinable/avyaya-like prefix or particle.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_rule import SamasaRule


class AvyayibhavaRule(
    SamasaRule,
):
    """
    Heuristic Avyayībhāva compound rule.
    """

    _AVYAYA_PREFIXES: tuple[str, ...] = (
        "उप",
        "प्रति",
        "अधि",
        "अभि",
        "अति",
        "अनु",
        "अपि",
        "सम्",
        "नि",
        "उद्",
        "परि",
        "प्र",
        "आ",
    )

    @property
    def display_name(self) -> str:
        return "Avyayibhava Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic rule for Avyayībhāva compounds."

    def _extract_text(self, context: SamasaContext) -> str:
        return str(context.subject).strip()

    def _hinted(self, context: SamasaContext) -> bool:
        hint = str(context.get("samasa_hint", "")).lower()
        return hint in {"avyayibhava", "avyayibhāva"}

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
        return left.startswith(self._AVYAYA_PREFIXES)

    def apply(self, context: SamasaContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = self._extract_text(context)
        left, right = text.split(maxsplit=1)

        return (
            {
                "type": "Avyayibhava",
                "compound": text,
                "members": (left, right),
                "analysis": f"indeclinable-head: {left} + {right}",
            },
        )
