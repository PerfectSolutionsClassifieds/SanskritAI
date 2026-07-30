from __future__ import annotations

"""
SanskritAI
==========

Tatpurusha Rule

Concrete heuristic rule for Tatpuruṣa compounds.

This is the first compound rule in the Samasa Kernel and is
intentionally conservative. It recognizes likely Tatpuruṣa
candidates using either explicit metadata hints or a small set
of structural cues.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_rule import SamasaRule


class TatpurushaRule(
    SamasaRule,
):
    """
    Heuristic Tatpuruṣa compound rule.
    """

    @property
    def display_name(self) -> str:
        return "Tatpurusha Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic rule for Tatpuruṣa compounds."

    def _extract_text(self, context: SamasaContext) -> str:
        return str(context.subject).strip()

    def _hinted(self, context: SamasaContext) -> bool:
        hint = str(context.get("samasa_hint", "")).lower()
        return hint in {"tatpurusha", "tat-purusha", "tatpuruṣa"}

    def applies_to(self, context: SamasaContext) -> bool:
        text = self._extract_text(context)
        if not text:
            return False

        if self._hinted(context):
            return True

        # Conservative heuristic: two-part compound without an
        # explicit coordinating conjunction.
        parts = text.split()
        if len(parts) != 2:
            return False

        if " च " in f" {text} " or " वा " in f" {text} ":
            return False

        return True

    def apply(self, context: SamasaContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = self._extract_text(context)
        left, right = text.split(maxsplit=1)

        return (
            {
                "type": "Tatpurusha",
                "compound": text,
                "members": (left, right),
                "analysis": f"{left} + {right}",
            },
        )
