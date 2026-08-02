from __future__ import annotations

"""
SanskritAI
==========

Bāhiraṅga Resolver

Purpose
-------

Complements AntarangaResolver.

This resolver explicitly prefers rules acting on
outer grammatical environments.

Normally it is consulted only after
AntaraṅgaResolver determines that the conflict
belongs to an external derivational stage.

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
class BahirangaResolver(
    PaninianConflictResolver,
):
    """
    Resolves conflicts by preferring
    the more external rule.
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

        winner = max(
            conflict.candidate_rules,
            key=self._depth,
        )

        return (winner,)

    @property
    def paribhasha(
        self,
    ) -> str:
        return "बहिरङ्ग"

    @property
    def english(
        self,
    ) -> str:
        return (
            "Prefers the more external "
            "grammatical operation."
        )

    def summary(
        self,
    ) -> dict:
        return {
            "resolver": self.display_name,
            "paribhasha": self.paribhasha,
            "english": self.english,
        }
