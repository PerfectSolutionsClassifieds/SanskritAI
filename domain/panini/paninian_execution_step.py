from __future__ import annotations

"""
SanskritAI
==========

Paninian Execution Step

Represents one immutable execution step in a
Paninian derivation.

Each step records

    • context before execution

    • rule applied

    • context after execution

This is the atomic building block of
PaninianExecutionTrace.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)


@dataclass(frozen=True, slots=True)
class PaninianExecutionStep(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    One immutable execution step.
    """

    before: PaninianDerivationContext

    rule: PaninianRule

    after: PaninianDerivationContext

    candidates: tuple[Any, ...] = field(
        default_factory=tuple,
    )

    notes: tuple[str, ...] = field(
        default_factory=tuple,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def display_name(self) -> str:
        return self.rule.sutra_number

    @property
    def display_text(self) -> str:
        return (
            f"{self.rule.sutra_number} — "
            f"{self.rule.sutra}"
        )

    @property
    def display_description(self) -> str:
        return self.rule.metadata.display_description

    @property
    def operation(self):
        return self.rule.metadata.operation

    @property
    def behaviour(self):
        return self.rule.behaviour

    @property
    def candidate_count(self) -> int:
        return len(self.candidates)

    def summary(self) -> dict[str, Any]:
        return {
            "sutra_number": self.rule.sutra_number,
            "operation": self.operation.name,
            "behaviour": self.behaviour.name,
            "candidates": self.candidate_count,
        }
