from __future__ import annotations

"""
SanskritAI
==========

Dhatu Pratyaya Concatenation Rule

Concrete derivation rule that combines a Dhatu and a Pratyaya
into a simple derived surface form.

This is the first working derivation rule in the Morphological
Derivation Kernel and provides a stable baseline output for
Dhatu + Pratyaya combinations.

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


class DhatuPratyayaConcatRule(
    DerivationRule,
):
    """
    Simple Dhatu + Pratyaya concatenation rule.
    """

    @property
    def display_name(self) -> str:
        return "Dhatu Pratyaya Concatenation Rule"

    @property
    def display_description(self) -> str:
        return (
            "Combines Dhatu and Pratyaya into a derived "
            "surface candidate."
        )

    def applies_to(
        self,
        context: DerivationContext,
    ) -> bool:
        return (
            context.dhatu is not None
            and context.pratyaya is not None
            and bool(str(context.dhatu.root).strip())
            and bool(str(context.pratyaya.pratyaya).strip())
        )

    def apply(
        self,
        context: DerivationContext,
    ) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        root = str(context.dhatu.root).strip()
        pratyaya = str(context.pratyaya.pratyaya).strip()
        surface = f"{root}{pratyaya}"

        return (
            {
                "type": "DirectConcatDerivation",
                "surface": surface,
                "dhatu": root,
                "pratyaya": pratyaya,
                "analysis": f"{root} + {pratyaya} -> {surface}",
                "confidence": 1.0,
            },
        )
