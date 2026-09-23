from __future__ import annotations

"""
SanskritAI
==========

Dhātu Selection Stage

The first executable stage of the Paninian Derivation Pipeline.

Responsibilities
----------------
• Validate that a Dhātu has been supplied.
• Select the working Dhātu.
• Initialize the derivational form.
• Record the stage in the derivation history.

This stage intentionally performs only the canonical
selection of the verbal root.

Later Paninian rules (It-saṃjñā, guṇa, āgama, etc.)
operate on the state produced here.

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


class DhatuSelectionStage(
    PaninianDerivationStage,
):
    """
    Selects the working Dhātu.

    This is always the first stage of a Paninian derivation.
    """

    @property
    def display_name(
        self,
    ) -> str:
        return "Dhātu Selection"

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Initializes the derivation from the "
            "selected verbal root."
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
        Executes only when a Dhātu is available.
        """
        return context.dhatu is not None

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:
        """
        Initializes the derivational form from the Dhātu.
        """

        if context.dhatu is None:
            raise ValueError(
                "Paninian derivation requires a Dhātu."
            )

        # Prefer a canonical root attribute if available.
        root = (
            getattr(context.dhatu, "root", None)
            or getattr(context.dhatu, "text", None)
            or getattr(context.dhatu, "surface_form", None)
            or str(context.dhatu)
        )

        # Preserve immutability.
        new_state = replace(
            state,
            current_form=root,
        )

        return new_state.with_form(
            root,
            stage_name=self.display_name,
        )
