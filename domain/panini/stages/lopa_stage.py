from __future__ import annotations

"""
SanskritAI

Lopa Stage

Rule-driven implementation of Paninian Lopa rules.
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class LopaStage(PaninianRuleDrivenStage):

    @property
    def display_name(self) -> str:
        return "Lopa"

    @property
    def display_description(self) -> str:
        return (
            "Applies Paninian Lopa rules using "
            "registered rule collections."
        )

    @property
    def rule_set_name(self) -> str:
        return "lopa"
