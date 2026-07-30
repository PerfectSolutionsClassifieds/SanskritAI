from __future__ import annotations

"""
SanskritAI

Āgama Stage

Rule-driven implementation of Paninian augment rules.
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class AgamaStage(PaninianRuleDrivenStage):

    @property
    def display_name(self) -> str:
        return "Āgama"

    @property
    def display_description(self) -> str:
        return (
            "Applies Paninian Āgama rules using the "
            "registered rule repository."
        )

    @property
    def rule_set_name(self) -> str:
        return "agama"
