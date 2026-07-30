from __future__ import annotations

"""
SanskritAI
==========

Aṅga Processing Stage

Canonical Phase-2 stage of the Paninian Derivation Pipeline.

Purpose
-------
This stage establishes the current derivational base
(अङ्ग) upon which the majority of later Paninian rules
operate.

The stage itself intentionally performs almost no
transformations.

Instead, it

    • determines the current grammatical base,
    • records it in derivational metadata,
    • marks the transition into Aṅga processing,
    • prepares later stages
        - Guṇa
        - Vṛddhi
        - Āgama
        - Lopa
        - Substitution
        - Sandhi

Future versions will execute hundreds of Aṅga-related
Paninian rules contained in dedicated rule repositories.

Version
-------
v1.0.0
"""

from dataclasses import replace

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)
from SanskritAI.domain.panini.paninian_derivation_stage import (
    PaninianDerivationStage,
)
from SanskritAI.domain.panini.paninian_derivation_state import (
    PaninianDerivationState,
)


class AngaProcessingStage(
    PaninianDerivationStage,
):
    """
    Establishes the current Aṅga.

    This stage is intentionally lightweight and acts as
    the entry point for all later Aṅga-related rules.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Aṅga Processing"

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Establishes the derivational Aṅga for "
            "subsequent Paninian operations."
        )

    # ---------------------------------------------------------
    # Applicability
    # ---------------------------------------------------------

    def is_applicable(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> bool:
        """
        Executes once a derivational form exists.
        """
        return bool(state.current_form)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _derive_anga(
        self,
        state: PaninianDerivationState,
    ) -> str:
        """
        Determines the current Aṅga.

        Initial implementation simply treats the current
        derivational form as the Aṅga.

        Future versions will introduce true Paninian
        Aṅga determination.
        """
        return state.current_form

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:

        anga = self._derive_anga(
            state,
        )

        metadata = dict(state.metadata)

        metadata["anga"] = anga
        metadata["anga_established"] = True
        metadata["anga_stage"] = self.display_name

        updated_state = replace(
            state,
            metadata=metadata,
        )

        return (
            updated_state
            .add_rule(self.display_name)
            .with_form(
                anga,
                stage_name=self.display_name,
            )
        )
