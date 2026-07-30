from __future__ import annotations

"""
SanskritAI
==========

Final Form Stage

Canonical final stage of the Paninian Derivation Pipeline.

Purpose
-------
Produces the final surface form after all grammatical,
phonological, and Tripādī transformations have completed.

This stage intentionally performs no further grammatical
transformations. Instead, it

    • marks derivation as complete
    • freezes the final surface form
    • records completion metadata
    • prepares the derivation result for downstream kernels

Downstream consumers include

    • Vakya Kernel
    • Semantic Kernel
    • Chandas Kernel
    • Alankara Kernel
    • Knowledge Graph Kernel

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


class FinalFormStage(PaninianDerivationStage):
    """
    Finalizes the derivation.

    No additional grammatical rules are executed.
    """

    @property
    def display_name(self) -> str:
        return "Final Form"

    @property
    def display_description(self) -> str:
        return (
            "Produces the completed surface form."
        )

    def is_applicable(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> bool:
        return bool(state.current_form)

    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:

        metadata = dict(state.metadata)

        metadata["derivation_complete"] = True
        metadata["final_surface_form"] = (
            state.current_form
        )

        updated = replace(
            state,
            metadata=metadata,
        )

        updated = updated.add_rule(
            self.display_name,
        )

        return updated.with_form(
            state.current_form,
            stage_name=self.display_name,
        )
