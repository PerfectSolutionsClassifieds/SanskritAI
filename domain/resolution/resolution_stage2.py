from __future__ import annotations

"""
SanskritAI
==========

Resolution Stage

Defines one executable stage within the canonical
Resolution Pipeline.

A ResolutionStage owns exactly one linguistic service.

It receives a shared ResolutionState, enriches it,
and returns the same state.

The stage itself contains no linguistic reasoning.

Relationship
------------

ResolutionPipeline
        │
        ▼
ResolutionStage
        │
        ▼
ResolutionService
        │
        ▼
ResolutionState

Version
-------
v2.0.0
"""

from dataclasses import dataclass
from typing import Protocol

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.resolution.resolution_state import (
    ResolutionState,
)


class ResolutionService(Protocol):
    """
    Protocol implemented by all resolution services.
    """

    def resolve(
        self,
        state: ResolutionState,
    ) -> ResolutionState:
        ...


@dataclass(frozen=True, slots=True)
class ResolutionStage(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    One executable stage within the canonical pipeline.
    """

    name: str

    service: ResolutionService

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.name

    @property
    def display_description(self) -> str:
        return (
            f"{self.name} Resolution Stage"
        )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        state: ResolutionState,
    ) -> ResolutionState:
        """
        Executes this stage.

        The service enriches the supplied ResolutionState.
        """

        try:
            state = self.service.resolve(state)
            state.mark_completed(self.name)

        except Exception as exc:

            state.mark_failed(self.name)

            state.set_metadata(
                f"{self.name}.exception",
                str(exc),
            )

            raise

        return state

    def __str__(self) -> str:
        return self.display_text
