from __future__ import annotations

"""
SanskritAI

Tripādī Stage

Rule-driven implementation of the final Tripādī
transformations (Aṣṭādhyāyī 8.2–8.4).
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class TripadiStage(PaninianRuleDrivenStage):

    @property
    def display_name(self) -> str:
        return "Tripādī"

    @property
    def display_description(self) -> str:
        return (
            "Executes the ordered Tripādī rule collections."
        )

    @property
    def rule_set_name(self) -> str:
        return "tripadi"
