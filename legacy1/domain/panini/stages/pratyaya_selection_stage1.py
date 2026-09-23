from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Selection Stage

Second canonical stage of the Paninian Derivation Pipeline.

Responsibilities
----------------
• Validate the supplied Pratyaya.
• Attach the selected Pratyaya to the current derivational
  state.
• Preserve the derivation as an immutable state transition.

This stage deliberately performs only the grammatical
selection and attachment of the affix.

Subsequent stages (It-Saṃjñā, Lopa, Āgama,
Substitution, etc.) operate on the state produced here.

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


class PratyayaSelectionStage(
    PaninianDerivationStage,
):
    """
    Attaches the selected Pratyaya to the working derivation.
    """

    @property
    def display_name(
        self,
    ) -> str:
        return "Pratyaya Selection"

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Attaches the selected Pratyaya to the "
            "working derivation."
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
        Executes only when a Pratyaya exists.
        """
        return context.pratyaya is not None

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _pratyaya_text(
        self,
        pratyaya,
    ) -> str:
        """
        Extracts the canonical textual representation of the
        Pratyaya.

        Compatible with existing SanskritAI domain objects.
        """

        return (
            getattr(pratyaya, "text", None)
            or getattr(pratyaya, "surface_form", None)
            or getattr(pratyaya, "value", None)
            or getattr(pratyaya, "identifier", None)
            or str(pratyaya)
        )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:
        """
        Attaches the selected Pratyaya.

        At this stage no It-mark removal, Sandhi,
        Guṇa, Vṛddhi or substitutions are performed.
        """

        if context.pratyaya is None:
            raise ValueError(
                "Paninian derivation requires a Pratyaya."
            )

        suffix = self._pratyaya_text(
            context.pratyaya,
        )

        current_form = state.current_form or ""

        combined = f"{current_form}{suffix}"

        new_state = replace(
            state,
            current_form=combined,
        )

        return (
            new_state
            .add_rule(self.display_name)
            .with_form(
                combined,
                stage_name=self.display_name,
            )
        )
