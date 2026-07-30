from __future__ import annotations

"""
SanskritAI
==========

Kartā Grammar Rule

Concrete grammar rule for detecting the kartā role.

This rule is intentionally heuristic and lightweight. It is
designed as the first concrete rule in the Grammar Kernel and
can later be replaced or refined by more sophisticated
grammar-aware logic.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.grammar.grammar_rule import GrammarRule


class KartaGrammarRule(
    GrammarRule,
):
    """
    Heuristic rule for kartā detection.
    """

    @property
    def display_name(self) -> str:
        return "Kartā Grammar Rule"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Heuristic grammar rule that detects kartā-like "
            "forms."
        )

    def _extract_text(self, subject: Any) -> str:
        if subject is None:
            return ""

        if hasattr(subject, "text"):
            return str(getattr(subject, "text"))

        if hasattr(subject, "display_text"):
            return str(getattr(subject, "display_text"))

        return str(subject)

    def applies_to(
        self,
        subject: Any,
    ) -> bool:
        text = self._extract_text(subject).strip()
        if not text:
            return False

        # Very small heuristic for Sanskrit nominative-like forms.
        return text.endswith(("ḥ", "H", "aḥ", "ah"))

    def apply(
        self,
        subject: Any,
    ) -> tuple[Any, ...]:
        if not self.applies_to(subject):
            return tuple()

        return ("कर्ता",)
