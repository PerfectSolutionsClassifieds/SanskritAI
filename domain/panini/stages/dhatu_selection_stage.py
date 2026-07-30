from __future__ import annotations

"""
SanskritAI
==========

Dhātu Selection Stage

Canonical Paninian derivation stage responsible for selecting
the appropriate verbal root (धातु).

This stage no longer contains derivational logic.

All grammatical intelligence resides in the registered
PaninianRule objects belonging to the rule set

    dhatu_selection

The stage is therefore merely an orchestration layer.

Architecture

PaninianDerivationPipeline
        ↓
DhatuSelectionStage
        ↓
PaninianRuleDrivenStage
        ↓
PaninianRuleEngine
        ↓
PaninianRuleSet
        ↓
PaninianRule

Version
-------
v2.0.0
"""

from SanskritAI.domain.panini.stages.paninian_rule_driven_stage import (
    PaninianRuleDrivenStage,
)


class DhatuSelectionStage(
    PaninianRuleDrivenStage,
):
    """
    Executes the canonical Dhātu Selection phase.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Dhātu Selection"

    @property
    def display_description(self) -> str:
        return (
            "Selects the canonical dhātu using "
            "registered Paninian rules."
        )

    # ---------------------------------------------------------
    # Rule Set
    # ---------------------------------------------------------

    @property
    def rule_set_name(self) -> str:
        """
        Repository identifier of the rule set executed by
        this stage.
        """
        return "dhatu_selection"
