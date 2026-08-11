from __future__ import annotations

"""
SanskritAI
==========

Resolution Pipeline

Canonical orchestration engine.

The pipeline owns an ordered collection of ResolutionStage
objects.

Each stage enriches a shared ResolutionResult.

The pipeline itself contains no linguistic knowledge.

Pipeline

ResolutionContext
        │
        ▼
ResolutionPipeline
        │
        ├── Lexical
        ├── Morphology
        ├── Sandhi
        ├── Samasa
        ├── Semantic
        ├── Pragmatics (future)
        └── Commentary (future)
                │
                ▼
ResolutionResult

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

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
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical linguistic resolution pipeline.
    """

    stages: tuple[
        ResolutionStage,
        ...
    ] = field(default_factory=tuple)

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Resolution Pipeline"

    @property
    def display_text(self) -> str:
        return f"{len(self.stages)} Stages"

    @property
    def display_description(self) -> str:
        return (
            "Canonical linguistic resolution pipeline."
        )

    # ---------------------------------------------------------
    # Pipeline
    # ---------------------------------------------------------

    def execute(
        self,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Executes the pipeline.

        Every stage enriches the same ResolutionResult.
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
    # Collection API
    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[ResolutionStage]:
        return iter(self.stages)

    def __len__(
        self,
    ) -> int:
        return len(self.stages)

    def __getitem__(
        self,
        index: int,
    ) -> ResolutionStage:
        return self.stages[index]

    @property
    def count(self) -> int:
        return len(self.stages)

    @property
    def is_empty(self) -> bool:
        return len(self.stages) == 0

    def __str__(self) -> str:
        return self.display_text
