from __future__ import annotations

"""
SanskritAI
==========

Bahuvrihi Rule

Concrete heuristic rule for Bahuvrīhi compounds.

This rule uses a small set of hints and structural cues to
identify likely possessive compounds. It is intentionally
conservative and can later be refined with deeper lexical and
grammatical analysis.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_rule import SamasaRule


class BahuvrihiRule(
    SamasaRule,
):
    """
    Heuristic Bahuvrīhi compound rule.
    """

    @property
    def display_name(self) -> str:
        return "Bahuvrihi Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic rule for Bahuvrīhi compounds."

    def _extract_text(self, context: SamasaContext) -> str:
        return str(context.subject).strip()

    def _hinted(self, context: SamasaContext) -> bool:
        hint = str(context.get("samasa_hint", "")).lower()
        return hint in {"bahuvrihi", "bahuvrīhi"}

    def applies_to(self, context: SamasaContext) -> bool:
        text = self._extract_text(context)
        if not text:
            return False

        if self._hinted(context):
            return True

        parts = text.split()
        if len(parts) != 2:
            return False

        left, right = parts

        possessive_cues = (
            "मह", "सु", "दु", "निष्", "सु", "अति", "अल्प", "बहु"
        )

        return left.startswith(possessive_cues) or right.endswith(("वत्", "मान", "युक्त"))

    def apply(self, context: SamasaContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = self._extract_text(context)
        left, right = text.split(maxsplit=1)

        return (
            {
                "type": "Bahuvrihi",
                "compound": text,
                "members": (left, right),
                "analysis": f"possessor-of: {left} + {right}",
            },
        )
