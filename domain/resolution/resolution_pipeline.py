from __future__ import annotations

"""
SanskritAI
==========

Resolution Pipeline

Canonical orchestration pipeline for Sanskrit linguistic
analysis.

Pipeline

ResolutionContext
        │
        ▼
ResolutionResult(context)
        │
        ▼
Lexical
        ▼
Morphology
        ▼
Sandhi
        ▼
Samasa
        ▼
Semantic
        ▼
Future:
    Pragmatics
    Commentary
    Reasoning

Each stage enriches the SAME immutable ResolutionResult.

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)
from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)
from SanskritAI.domain.resolution.resolution_stage import (
    ResolutionStage,
)


@dataclass(frozen=True, slots=True)
class ResolutionPipeline(
    Displayable,
):
    """
    Canonical linguistic resolution pipeline.
    """

    stages: tuple[
        ResolutionStage,
        ...
    ] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Resolution Pipeline"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical Sanskrit linguistic resolution "
            "pipeline."
        )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def stage_count(self) -> int:
        return len(self.stages)

    @property
    def is_empty(self) -> bool:
        return self.stage_count == 0

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Executes the complete linguistic pipeline.

        Every stage enriches the same immutable
        ResolutionResult.
        """

        result = ResolutionResult(
            context=context,
        )

        for stage in self.stages:
            result = stage.execute(
                result,
            )

        return result

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(self):
        return iter(self.stages)

    def __len__(self) -> int:
        return self.stage_count

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
