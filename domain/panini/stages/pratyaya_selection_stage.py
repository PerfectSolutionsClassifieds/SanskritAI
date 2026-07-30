from __future__ import annotations

"""
SanskritAI

Pratyaya Selection Stage

Rule-driven stage responsible for selecting the appropriate
pratyaya using registered Paninian rules.
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class PratyayaSelectionStage(PaninianRuleDrivenStage):

    @property
    def display_name(self) -> str:
        return "Pratyaya Selection"

    @property
    def display_description(self) -> str:
        return (
            "Selects the appropriate pratyaya using "
            "registered Paninian rules."
        )

    @property
    def rule_set_name(self) -> str:
        return "pratyaya_selection"
