from __future__ import annotations

"""
SanskritAI
==========

Visarga To R Rule

Implements the common Visarga → र transformation.

Hierarchy
---------

VisargaSandhiRule
        │
        ▼
VisargaTransformationRule
        │
        ▼
VisargaToRRule

Version
-------
v1.0.0
"""

from SanskritAI.domain.sandhi.sandhi_context import SandhiContext
from SanskritAI.domain.sandhi.visarga_transformation_rule import (
    VisargaTransformationRule,
)


class VisargaToRRule(
    VisargaTransformationRule,
):

    @property
    def display_name(self) -> str:
        return "Visarga To R Rule"

    @property
    def display_description(self) -> str:
        return (
            "Transforms Visarga into Repha."
        )

    def _extract_words(
        self,
        context: SandhiContext,
    ) -> tuple[str, str] | None:

        parts = str(context.subject).split()

        if len(parts) != 2:
            return None

        return parts[0], parts[1]

    def applies_to(
        self,
        context: SandhiContext,
    ) -> bool:

        words = self._extract_words(context)

        if words is None:
            return False

        left, _ = words

        return left.endswith("ः")

    def apply(
        self,
        context: SandhiContext,
    ) -> tuple[str, ...]:

        words = self._extract_words(context)

        if words is None:
            return tuple()

        left, right = words

        if not left.endswith("ः"):
            return tuple()

        return (
            left[:-1] + "र" + right,
        )
