from __future__ import annotations

"""
SanskritAI
==========

Hint Based Derivation Rule

Concrete derivation rule that uses explicit metadata hints to
produce a derived form candidate.

This rule is useful when the caller already knows the target
surface shape and wants the kernel to normalize or package it
as a derivation candidate.

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


class HintBasedDerivationRule(
    DerivationRule,
):
    """
    Metadata-driven derivation rule.
    """

    @property
    def display_name(self) -> str:
        return "Hint Based Derivation Rule"

    @property
    def display_description(self) -> str:
        return (
            "Produces a derivation candidate from explicit "
            "metadata hints."
        )

    def applies_to(
        self,
        context: DerivationContext,
    ) -> bool:
        return bool(
            context.get("derived_form", "")
            or context.get("surface", "")
            or context.get("output", "")
        )

    def apply(
        self,
        context: DerivationContext,
    ) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        surface = str(
            context.get("derived_form", "")
            or context.get("surface", "")
            or context.get("output", "")
        ).strip()

        if not surface:
            return tuple()

        return (
            {
                "type": "HintBasedDerivation",
                "surface": surface,
                "dhatu": str(context.dhatu.root).strip(),
                "pratyaya": str(context.pratyaya.pratyaya).strip(),
                "analysis": surface,
                "confidence": float(context.get("confidence", 0.75)),
            },
        )
