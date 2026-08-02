from __future__ import annotations

"""
SanskritAI
==========

Vipratiṣedha Resolver

Implements the classical Paribhāṣā

    विप्रतिषेधे परं कार्यम्

"When two rules are in conflict,
the later rule operates."

(Aṣṭādhyāyī 1.4.2)

Purpose
-------

This resolver is the primary conflict-resolution
strategy of the Paninian grammar engine.

Given multiple simultaneously applicable rules,
the resolver selects the rule occurring later in
the canonical order of the Aṣṭādhyāyī.

Current Ordering
----------------

The first implementation compares rules by

    1. Adhyāya
    2. Pāda
    3. Sūtra Number

Future versions may additionally incorporate

• Asiddha domains

• Adhikāra scope

• Rule priority

• Classical Paribhāṣā interactions

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
class VipratisedhaResolver(
    PaninianConflictResolver,
):
    """
    Implements

        विप्रतिषेधे परं कार्यम्
    """

    # ---------------------------------------------------------
    # Capability
    # ---------------------------------------------------------

    def supports(
        self,
        conflict: PaninianRuleConflict,
    ) -> bool:
        """
        Applicable whenever more than one rule
        simultaneously matches.
        """

        return conflict.has_conflict

    # ---------------------------------------------------------
    # Internal ordering
    # ---------------------------------------------------------

    @staticmethod
    def _ordering_key(
        rule: PaninianRule,
    ) -> tuple[int, int, tuple[int, ...]]:
        """
        Canonical ordering key.

        Rules later in the Aṣṭādhyāyī are considered
        greater.

        Sūtra numbers are parsed numerically.

        Example

            6.1.77

        becomes

            (6, 1, (6, 1, 77))
        """

        parts = tuple(
            int(x)
            for x in rule.sutra_number.split(".")
            if x.isdigit()
        )

        return (
            rule.adhyaya,
            rule.pada,
            parts,
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        conflict: PaninianRuleConflict,
    ) -> tuple[PaninianRule, ...]:
        """
        Selects the later rule.

        Returns
        -------
        tuple[PaninianRule, ...]

        Always returns a single rule.
        """

        if conflict.is_empty:
            return ()

        if conflict.rule_count == 1:
            return conflict.candidate_rules

        winner = max(
            conflict.candidate_rules,
            key=self._ordering_key,
        )

        return (winner,)

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def paribhasha(
        self,
    ) -> str:
        return "विप्रतिषेधे परं कार्यम्"

    @property
    def english(
        self,
    ) -> str:
        return (
            "When rules conflict, "
            "the later rule applies."
        )

    def summary(
        self,
    ) -> dict:
        return {
            "resolver": self.display_name,
            "paribhasha": self.paribhasha,
            "english": self.english,
        }
