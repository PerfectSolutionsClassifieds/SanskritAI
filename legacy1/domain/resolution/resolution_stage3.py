from __future__ import annotations

"""
SanskritAI
==========

Resolution Stage

A ResolutionStage enriches an existing ResolutionResult.

Pipeline

ResolutionResult
        │
        ▼
ResolutionStage
        │
        ▼
ResolutionResult

Every stage is responsible for exactly ONE linguistic kernel.

Version
-------
v2.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


@dataclass(frozen=True, slots=True)
class ResolutionStage(
    Displayable,
):
    """
    One stage of the linguistic resolution pipeline.
    """

    name: str

    service: object

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
            f"Resolution stage: {self.name}"
        )

    # ---------------------------------------------------------

    def execute(
        self,
        result: ResolutionResult,
    ) -> ResolutionResult:
        """
        Enriches the supplied ResolutionResult.

        The concrete service returns a domain-specific
        ResolutionResult which is merged into the aggregate.
        """

        stage_result = self.service.resolve(
            result.context,
        )

        stage_name = self.name.lower()

        if stage_name == "lexical":
            return result.with_lexical(stage_result)

        if stage_name == "morphology":
            return result.with_morphology(stage_result)

        if stage_name == "sandhi":
            return result.with_sandhi(stage_result)

        if stage_name == "samasa":
            return result.with_samasa(stage_result)

        if stage_name == "semantic":
            return result.with_semantic(stage_result)

        return result

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
