from __future__ import annotations

"""
SanskritAI

It-Saṃjñā Stage

Rule-driven implementation of Paninian It-marker
identification.
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class ItSamjnaStage(PaninianRuleDrivenStage):

    @property
    def display_name(self) -> str:
        return "It-Saṃjñā"

    @property
    def display_description(self) -> str:
        return (
            "Identifies It markers using registered "
            "Paninian rules."
        )

    @property
    def rule_set_name(self) -> str:
        return "it_samjna"
