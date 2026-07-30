from __future__ import annotations

"""
SanskritAI

Aṅga Processing Stage

Rule-driven implementation of Aṅga establishment.
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class AngaProcessingStage(PaninianRuleDrivenStage):

    @property
    def display_name(self) -> str:
        return "Aṅga Processing"

    @property
    def display_description(self) -> str:
        return (
            "Processes the derivational Aṅga using "
            "registered Paninian rules."
        )

    @property
    def rule_set_name(self) -> str:
        return "anga_processing"
