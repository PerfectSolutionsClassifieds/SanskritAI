from __future__ import annotations

"""
SanskritAI
==========

Dvandva Rule

Concrete heuristic rule for Dvandva compounds.

This rule recognizes coordinating patterns such as
'X च Y' and 'X वा Y', or explicit metadata hints.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_rule import SamasaRule


class DvandvaRule(
    SamasaRule,
):
    """
    Heuristic Dvandva compound rule.
    """

    @property
    def display_name(self) -> str:
        return "Dvandva Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic rule for Dvandva compounds."

    def _extract_text(self, context: SamasaContext) -> str:
        return str(context.subject).strip()

    def _hinted(self, context: SamasaContext) -> bool:
        hint = str(context.get("samasa_hint", "")).lower()
        return hint in {"dvandva", "dvaṇḍva"}

    def applies_to(self, context: SamasaContext) -> bool:
        text = self._extract_text(context)
        if not text:
            return False

        if self._hinted(context):
            return True

        padded = f" {text} "
        return (" च " in padded) or (" वा " in padded)

    def apply(self, context: SamasaContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = self._extract_text(context)
        padded = f" {text} "

        if " च " in padded:
            members = tuple(part for part in text.split(" च ") if part.strip())
        elif " वा " in padded:
            members = tuple(part for part in text.split(" वा ") if part.strip())
        else:
            members = tuple(part for part in text.split() if part.strip())

        return (
            {
                "type": "Dvandva",
                "compound": text,
                "members": members,
                "analysis": " + ".join(members),
            },
        )
