from __future__ import annotations

"""
SanskritAI
==========

Resolution Stage

A ResolutionStage is a thin orchestration wrapper around a
ResolutionContributor.

It owns no linguistic logic.

Responsibilities
----------------

• execute one pipeline stage

• delegate to the underlying contributor

• preserve ordering inside ResolutionPipeline

The stage never needs modification when new linguistic
kernels are added.

Version
-------
v3.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_contributor import (
    ResolutionContributor,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ResolutionStage(
    Displayable,
):
    """
    Thin wrapper around a ResolutionContributor.
    """

    contributor: ResolutionContributor

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return self.contributor.display_name

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
            f"Pipeline stage using "
            f"{self.contributor.display_name}."
        )

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        aggregate: ResolutionResult,
    ) -> ResolutionResult:
        """
        Executes one pipeline stage.

        The contributor performs all linguistic work and
        returns an enriched immutable ResolutionResult.
        """

        return self.contributor.contribute(
            aggregate=aggregate,
            context=aggregate.context,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def context_type(
        self,
    ) -> type[ResolutionContext]:
        return ResolutionContext

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
