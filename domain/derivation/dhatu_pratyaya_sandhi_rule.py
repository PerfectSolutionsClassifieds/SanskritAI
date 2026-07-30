from __future__ import annotations

"""
SanskritAI
==========

Dhatu Pratyaya Sandhi Rule

Concrete derivation rule that combines a Dhatu and a Pratyaya
with a small set of sandhi-aware rewrite heuristics.

This enriches the Morphological Derivation Kernel beyond
simple concatenation while remaining conservative and easy to
extend.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.derivation.derivation_context import (
    DerivationContext,
)
from SanskritAI.domain.derivation.derivation_rule import (
    DerivationRule,
)


class DhatuPratyayaSandhiRule(
    DerivationRule,
):
    """
    Sandhi-aware derivation rule.
    """

    _REWRITE_TABLE: tuple[tuple[str, str, str], ...] = (
        ("अ", "अ", "आ"),
        ("आ", "अ", "आ"),
        ("अ", "इ", "ए"),
        ("अ", "ई", "ए"),
        ("अ", "उ", "ओ"),
        ("अ", "ऊ", "ओ"),
        ("भू", "क्त", "भूत"),
        ("गम्", "क्त", "गत"),
        ("कृ", "क्त", "कृत"),
        ("गम्", "ल्यप्", "गत्वा"),
        ("कृ", "ल्यप्", "कृत्वा"),
    )

    @property
    def display_name(self) -> str:
        return "Dhatu Pratyaya Sandhi Rule"

    @property
    def display_description(self) -> str:
        return (
            "Combines Dhatu and Pratyaya using conservative "
            "sandhi-aware rewrite heuristics."
        )

    def _key(
        self,
        context: DerivationContext,
    ) -> tuple[str, str]:
        return (
            str(context.dhatu.root).strip(),
            str(context.pratyaya.pratyaya).strip(),
        )

    def applies_to(
        self,
        context: DerivationContext,
    ) -> bool:
        return any(
            self._key(context) == (left, right)
            for left, right, _ in self._REWRITE_TABLE
        )

    def apply(
        self,
        context: DerivationContext,
    ) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        root, pratyaya = self._key(context)

        outputs: list[Any] = []

        for left, right, surface in self._REWRITE_TABLE:
            if (root, pratyaya) == (left, right):
                outputs.append(
                    {
                        "type": "SandhiAwareDerivation",
                        "surface": surface,
                        "dhatu": root,
                        "pratyaya": pratyaya,
                        "analysis": f"{root} + {pratyaya} -> {surface}",
                        "confidence": 1.0,
                    }
                )

        return tuple(outputs)
