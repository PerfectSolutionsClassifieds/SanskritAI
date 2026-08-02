from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Match Result

Represents the outcome of attempting to match a Paninian rule
against a derivation context.

This object is intentionally immutable and independent of any
particular grammatical kernel. It is consumed by the rule
execution engine to determine whether a rule should be applied.

Architecture
------------

PaninianRule
        │
        ▼
RuleMatcher
        │
        ▼
PaninianRuleMatchResult
        │
        ▼
RuleExecutionEngine

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_rule import PaninianRule


@dataclass(frozen=True, slots=True)
class PaninianRuleMatchResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Result returned by a PaninianRuleMatcher.
    """

    rule: PaninianRule

    matched: bool

    score: float = 1.0

    confidence: float = 1.0

    matched_conditions: tuple[str, ...] = field(
        default_factory=tuple,
    )

    failed_conditions: tuple[str, ...] = field(
        default_factory=tuple,
    )

    diagnostics: tuple[str, ...] = field(
        default_factory=tuple,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Rule Match Result"

    @property
    def display_text(self) -> str:
        status = "MATCH" if self.matched else "NO MATCH"

        return (
            f"{status} : "
            f"{self.rule.sutra_number}"
        )

    @property
    def display_description(self) -> str:
        return self.rule.sutra

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_match(self) -> bool:
        return self.matched

    @property
    def is_not_match(self) -> bool:
        return not self.matched

    @property
    def has_failures(self) -> bool:
        return len(self.failed_conditions) > 0

    @property
    def has_diagnostics(self) -> bool:
        return len(self.diagnostics) > 0

    @property
    def matched_condition_count(self) -> int:
        return len(self.matched_conditions)

    @property
    def failed_condition_count(self) -> int:
        return len(self.failed_conditions)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def total_condition_count(self) -> int:
        return (
            self.matched_condition_count
            + self.failed_condition_count
        )

    @property
    def canonical_reference(self) -> str:
        return self.rule.sutra_number

    # ---------------------------------------------------------
    # Ordering
    # ---------------------------------------------------------

    def __lt__(
        self,
        other: "PaninianRuleMatchResult",
    ) -> bool:
        """
        Higher score wins.
        """
        return self.score < other.score

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __bool__(self) -> bool:
        return self.matched

    def __str__(self) -> str:
        return self.display_text
