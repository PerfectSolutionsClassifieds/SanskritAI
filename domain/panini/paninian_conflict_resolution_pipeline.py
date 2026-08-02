from __future__ import annotations

"""
SanskritAI
==========

Paninian Conflict Resolution Pipeline

Canonical orchestration layer for Paninian
Paribhāṣā-based conflict resolution.

Purpose
-------

Rather than applying a single resolver, the
pipeline executes a sequence of conflict
resolvers.

Example
-------

VipratisedhaResolver
        ↓
AntarangaResolver
        ↓
BahirangaResolver
        ↓
NityaResolver
        ↓
AsiddhaResolver
        ↓
OptionalRuleResolver

Each resolver receives the remaining candidate
rules and may reduce them further.

Architecture
------------

PaninianRuleConflict
        │
        ▼
PaninianConflictResolutionPipeline
        │
        ├── VipratisedhaResolver
        ├── AntarangaResolver
        ├── BahirangaResolver
        ├── NityaResolver
        ├── AsiddhaResolver
        └── OptionalRuleResolver

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)

from SanskritAI.domain.panini.paninian_rule_conflict import (
    PaninianRuleConflict,
)

from SanskritAI.domain.panini.paninian_conflict_resolver import (
    PaninianConflictResolver,
)


@dataclass(slots=True)
class PaninianConflictResolutionPipeline:
    """
    Canonical Paribhāṣā resolution pipeline.
    """

    resolvers: tuple[
        PaninianConflictResolver,
        ...
    ] = field(
        default_factory=tuple,
    )

    execution_history: list[dict[str, Any]] = field(
        default_factory=list,
    )

    # ---------------------------------------------------------
    # Pipeline execution
    # ---------------------------------------------------------

    def resolve(
        self,
        conflict: PaninianRuleConflict,
    ) -> tuple[PaninianRule, ...]:
        """
        Applies all applicable resolvers.

        Returns
        -------
        tuple[PaninianRule, ...]
        """

        current_rules = (
            conflict.candidate_rules
        )

        current_conflict = conflict

        for resolver in self.resolvers:

            if len(current_rules) <= 1:
                break

            if not resolver.supports(
                current_conflict,
            ):
                continue

            resolved = resolver.resolve(
                current_conflict,
            )

            self.execution_history.append(
                {
                    "resolver": (
                        resolver.display_name
                    ),
                    "before": len(
                        current_rules
                    ),
                    "after": len(
                        resolved
                    ),
                }
            )

            current_rules = resolved

            current_conflict = (
                PaninianRuleConflict(
                    context=conflict.context,
                    candidate_rules=current_rules,
                )
            )

        return current_rules

    # ---------------------------------------------------------
    # Builder helpers
    # ---------------------------------------------------------

    def add_resolver(
        self,
        resolver: PaninianConflictResolver,
    ) -> None:
        """
        Dynamically adds resolver.

        Mostly useful for testing.
        """

        self.resolvers = (
            self.resolvers + (resolver,)
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def resolver_count(
        self,
    ) -> int:
        return len(
            self.resolvers
        )

    def clear_history(
        self,
    ) -> None:
        self.execution_history.clear()

    def summary(
        self,
    ) -> dict:
        return {
            "resolver_count":
                self.resolver_count,
            "history_steps":
                len(
                    self.execution_history
                ),
            "resolvers":
                tuple(
                    r.display_name
                    for r in self.resolvers
                ),
        }

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:
        return self.resolver_count

    def __iter__(
        self,
    ):
        yield from self.resolvers

    def __str__(
        self,
    ) -> str:
        return (
            "PaninianConflictResolutionPipeline("
            f"{self.resolver_count} resolvers)"
        )
