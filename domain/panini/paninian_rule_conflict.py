from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Conflict

Represents a set of executable rules that
simultaneously match the same derivation context.

Resolution is performed by one or more
Paribhāṣā-based conflict resolvers.
"""

from dataclasses import dataclass

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)


@dataclass(frozen=True, slots=True)
class PaninianRuleConflict:
    """
    Immutable rule conflict.
    """

    context: PaninianDerivationContext

    candidate_rules: tuple[PaninianRule, ...]

    @property
    def rule_count(self) -> int:
        return len(self.candidate_rules)

    @property
    def is_empty(self) -> bool:
        return self.rule_count == 0

    @property
    def has_conflict(self) -> bool:
        return self.rule_count > 1

    def summary(self) -> dict:
        return {
            "rule_count": self.rule_count,
            "has_conflict": self.has_conflict,
        }
