from __future__ import annotations

"""
SanskritAI

Substitution Stage

Rule-driven implementation of Paninian Ādeśa rules.
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class SubstitutionStage(PaninianRuleDrivenStage):

    @property
    def display_name(self) -> str:
        return "Substitution"

    @property
    def display_description(self) -> str:
        return (
            "Applies Paninian substitution (Ādeśa) rules."
        )

    @property
    def rule_set_name(self) -> str:
        return "substitution"
