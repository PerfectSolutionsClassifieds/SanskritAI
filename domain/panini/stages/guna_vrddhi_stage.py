from __future__ import annotations

"""
SanskritAI

Guṇa–Vṛddhi Stage

Rule-driven implementation of Guṇa and Vṛddhi transformations.
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class GunaVrddhiStage(PaninianRuleDrivenStage):

    @property
    def display_name(self) -> str:
        return "Guṇa–Vṛddhi"

    @property
    def display_description(self) -> str:
        return (
            "Applies Guṇa and Vṛddhi transformations using "
            "registered Paninian rules."
        )

    @property
    def rule_set_name(self) -> str:
        return "guna_vrddhi"
