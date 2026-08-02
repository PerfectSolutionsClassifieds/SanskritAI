from __future__ import annotations

"""
SanskritAI
==========

Antaraṅga Resolver

Implements the classical Paribhāṣā

    अन्तरङ्गं बहिरङ्गाद् बलीयः

"The internally operating rule is stronger than
the externally operating rule."

Purpose
-------

Prefers rules acting on a more internal grammatical
environment.

Current implementation assumes that smaller
'derivation_depth' values indicate more internal
operations.

Future versions may compute true grammatical
interiority from derivation graphs.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.panini.paninian_conflict_resolver import (
    PaninianConflictResolver,
)
from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)
from SanskritAI.domain.panini.paninian_rule_conflict import (
    PaninianRuleConflict,
)


@dataclass(frozen=True, slots=True)
class AntarangaResolver(
    PaninianConflictResolver,
):
    """
    Implements

        अन्तरङ्गं बहिरङ्गाद् बलीयः
    """

    def supports(
        self,
        conflict: PaninianRuleConflict,
    ) -> bool:
        return conflict.has_conflict

    @staticmethod
    def _depth(
        rule: PaninianRule,
    ) -> int:
        """
        Lower depth = more internal.

        Default = large value.
        """

        return int(
            rule.metadata.metadata.get(
                "derivation_depth",
                1000,
            )
        )

    def resolve(
        self,
        conflict: PaninianRuleConflict,
    ) -> tuple[PaninianRule, ...]:

        if conflict.is_empty:
            return ()

        if conflict.rule_count == 1:
            return conflict.candidate_rules

        winner = min(
            conflict.candidate_rules,
            key=self._depth,
        )

        return (winner,)

    @property
    def paribhasha(
        self,
    ) -> str:
        return "अन्तरङ्गं बहिरङ्गाद् बलीयः"

    @property
    def english(
        self,
    ) -> str:
        return (
            "Internal operations are stronger "
            "than external operations."
        )

    def summary(
        self,
    ) -> dict:
        return {
            "resolver": self.display_name,
            "paribhasha": self.paribhasha,
            "english": self.english,
        }
