from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Stage

Abstract base class for every stage in the Paninian
Derivation Pipeline.

A stage represents one canonical phase of the derivational
process described in the Aṣṭādhyāyī.

Typical stages include

    • Dhātu Selection
    • Pratyaya Selection
    • It-Saṃjñā
    • Aṅga Processing
    • Guṇa / Vṛddhi
    • Morphological Operations
    • Sandhi
    • Tripādī
    • Final Surface Form

Every stage is:

    Input
        PaninianDerivationState
            │
            ▼
        apply(...)
            │
            ▼
    New PaninianDerivationState

Stages NEVER mutate an existing state.

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.panini.paninian_derivation_context import (
    PaninianDerivationContext,
)
from SanskritAI.domain.panini.paninian_derivation_state import (
    PaninianDerivationState,
)


class PaninianDerivationStage(
    Displayable,
    ABC,
):
    """
    Base class for one derivational stage.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def display_name(
        self,
    ) -> str:
        """
        Human-readable stage name.
        """

    @property
    def display_text(
        self,
    ) -> str:
        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Paninian derivation stage."
        )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    @property
    def stage_name(
        self,
    ) -> str:
        return self.display_name

    @property
    def stage_identifier(
        self,
    ) -> str:
        return (
            self.display_name
            .lower()
            .replace(" ", "_")
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
        Returns whether this stage should execute.

        Concrete stages may override this.

        Default
        -------
        Always applicable.
        """
        return True

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    @abstractmethod
    def apply(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:
        """
        Executes this stage.

        Parameters
        ----------
        context
            Immutable derivation context.

        state
            Current derivation state.

        Returns
        -------
        PaninianDerivationState

        The next immutable derivation state.
        """

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def execute(
        self,
        context: PaninianDerivationContext,
        state: PaninianDerivationState,
    ) -> PaninianDerivationState:
        """
        Executes the stage if applicable.

        If not applicable, the incoming state is returned
        unchanged.
        """

        if not self.is_applicable(
            context,
            state,
        ):
            return state

        result = self.apply(
            context,
            state,
        )

        return (
            result
            .add_rule(self.display_name)
            .with_form(
                result.current_form,
                stage_name=self.display_name,
            )
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
