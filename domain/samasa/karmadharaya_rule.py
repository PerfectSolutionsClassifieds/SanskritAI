from __future__ import annotations

"""
SanskritAI
==========

Karmadharaya Rule

Concrete heuristic rule for Karmadhāraya compounds.

This rule uses a small set of modifier-like prefixes and
metadata hints to identify likely Karmadhāraya compounds.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_rule import SamasaRule


class KarmadharayaRule(
    SamasaRule,
):
    """
    Heuristic Karmadhāraya compound rule.
    """

    _COMMON_MODIFIER_PREFIXES: tuple[str, ...] = (
        "महा",
        "सु",
        "दु",
        "अति",
        "उप",
        "अधि",
        "निर",
        "नि",
        "परि",
        "प्र",
        "अव",
    )

    @property
    def display_name(self) -> str:
        return "Karmadharaya Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic rule for Karmadhāraya compounds."

    def _extract_text(self, context: SamasaContext) -> str:
        return str(context.subject).strip()

    def _hinted(self, context: SamasaContext) -> bool:
        hint = str(context.get("samasa_hint", "")).lower()
        return hint in {"karmadharaya", "karmadhāraya"}

    def applies_to(self, context: SamasaContext) -> bool:
        text = self._extract_text(context)
        if not text:
            return False

        if self._hinted(context):
            return True

        parts = text.split()
        if len(parts) != 2:
            return False

        left = parts[0]

        return left.startswith(self._COMMON_MODIFIER_PREFIXES)

    def apply(self, context: SamasaContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = self._extract_text(context)
        left, right = text.split(maxsplit=1)

        return (
            {
                "type": "Karmadharaya",
                "compound": text,
                "members": (left, right),
                "analysis": f"{left} ≈ {right}",
            },
        )
