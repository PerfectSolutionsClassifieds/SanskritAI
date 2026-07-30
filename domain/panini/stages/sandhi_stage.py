from __future__ import annotations

"""
SanskritAI

Sandhi Stage

Rule-driven implementation of Paninian Sandhi.
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class SandhiStage(PaninianRuleDrivenStage):

    @property
    def display_name(self) -> str:
        return "Sandhi"

    @property
    def display_description(self) -> str:
        return (
            "Executes Sandhi rules using the "
            "registered Paninian rule repository."
        )

    @property
    def rule_set_name(self) -> str:
        return "sandhi"
