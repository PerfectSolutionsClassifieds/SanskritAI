from __future__ import annotations

"""
SanskritAI
==========

Paninian Derivation Trace

Canonical immutable trace of the complete Paninian
Derivation Pipeline.

Unlike a simple log, this object preserves every
intermediate grammatical state generated during
derivation, allowing SanskritAI to explain exactly
how a final form was produced.

Pipeline

Initial State
      │
      ▼
Stage 1
      │
      ▼
State 1
      │
      ▼
Stage 2
      │
      ▼
State 2
      │
      ▼
...
      │
      ▼
Final State

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.panini.paninian_derivation_state import (
    PaninianDerivationState,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PaninianDerivationTrace(
    Displayable,
):
    """
    Immutable derivation history.

    Stores every PaninianDerivationState generated
    throughout the derivation process.
    """

    states: tuple[
        PaninianDerivationState,
        ...
    ] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Paninian Derivation Trace"

    @property
    def display_text(
        self,
    ) -> str:
        return (
            f"{self.display_name}"
            f" ({self.state_count} states)"
        )

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Immutable history of every derivational "
            "state produced by the Paninian "
            "Derivation Pipeline."
        )

    # ---------------------------------------------------------
    # Inspection
    # ---------------------------------------------------------

    @property
    def state_count(
        self,
    ) -> int:
        return len(
            self.states
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return self.state_count == 0

    @property
    def is_not_empty(
        self,
    ) -> bool:
        return not self.is_empty

    @property
    def first(
        self,
    ) -> PaninianDerivationState | None:
        if self.is_empty:
            return None

        return self.states[0]

    @property
    def last(
        self,
    ) -> PaninianDerivationState | None:
        if self.is_empty:
            return None

        return self.states[-1]

    @property
    def current_state(
        self,
    ) -> PaninianDerivationState | None:
        """
        Alias for the latest derivation state.
        """
        return self.last

    @property
    def current_form(
        self,
    ) -> str | None:
        """
        Returns the latest surface form.
        """
        if self.last is None:
            return None

        return self.last.current_form

    # ---------------------------------------------------------
    # Functional updates
    # ---------------------------------------------------------

    def add(
        self,
        state: PaninianDerivationState,
    ) -> "PaninianDerivationTrace":
        """
        Returns a new trace containing the supplied
        derivation state.
        """

        return PaninianDerivationTrace(
            states=(
                *self.states,
                state,
            )
        )

    def extend(
        self,
        states: tuple[
            PaninianDerivationState,
            ...
        ],
    ) -> "PaninianDerivationTrace":
        """
        Returns a new trace with additional states.
        """

        return PaninianDerivationTrace(
            states=(
                *self.states,
                *states,
            )
        )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def state_at(
        self,
        index: int,
    ) -> PaninianDerivationState:
        """
        Returns the state at the specified index.
        """
        return self.states[index]

    def stage_names(
        self,
    ) -> tuple[str, ...]:
        """
        Returns every executed stage.
        """
        return tuple(
            state.stage_name
            for state in self.states
        )

    def surface_forms(
        self,
    ) -> tuple[str, ...]:
        """
        Returns every intermediate surface form.
        """
        return tuple(
            state.current_form
            for state in self.states
        )

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(
        self,
    ):
        return iter(
            self.states
        )

    def __len__(
        self,
    ) -> int:
        return self.state_count

    def __getitem__(
        self,
        index: int,
    ) -> PaninianDerivationState:
        return self.states[index]

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
