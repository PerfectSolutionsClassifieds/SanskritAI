
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from SanskritAI.domain.derivation.derivation_rule import (
    DerivationContext,
    DerivationRule,
)


@dataclass(frozen=True)
class DerivationRuleSet:
    """
    Ordered collection of derivation rules.

    A rule set evaluates every rule that applies to a given
    derivation context and returns unique candidates while
    preserving their insertion order.

    Candidates are intentionally typed as ``Any`` because concrete
    derivation rules may return different candidate representations,
    including unhashable objects such as dictionaries.
    """

    rules: tuple[DerivationRule, ...] = ()

    def apply(
        self,
        context: DerivationContext,
    ) -> tuple[Any, ...]:
        """
        Applies every matching derivation rule and returns
        unique candidates in insertion order.

        Equality-based deduplication is used instead of
        hash-based deduplication because derivation candidates
        are not required to be hashable.
        """
        candidates: list[Any] = []

        for rule in self.rules:
            if rule.applies_to(context):
                candidates.extend(rule.apply(context))

        unique_candidates: list[Any] = []

        for candidate in candidates:
            if candidate not in unique_candidates:
                unique_candidates.append(candidate)

        return tuple(unique_candidates)
