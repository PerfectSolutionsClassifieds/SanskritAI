from __future__ import annotations

"""
SanskritAI
==========

Resolution Pipeline

The ResolutionPipeline is the canonical orchestration engine
for the SanskritAI linguistic stack.

It executes an ordered sequence of ResolutionStage objects,
allowing each stage to progressively enrich a shared
ResolutionContext.

Pipeline

    ResolutionContext
            │
            ▼
        Stage 1
            │
            ▼
        Stage 2
            │
            ▼
        Stage 3
            │
            ▼
        ...
            │
            ▼
    Enriched ResolutionContext

Typical configuration

    Lexical
        ↓
    Morphology
        ↓
    Sandhi
        ↓
    Samasa
        ↓
    Semantic
        ↓
    Pragmatics (future)
        ↓
    Commentarial Reasoning (future)

The pipeline itself contains no linguistic logic.

Its sole responsibility is orchestration.

Version
-------
v3.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
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
    Immutable orchestration pipeline.

    Each ResolutionStage receives the current
    ResolutionContext and returns an enriched
    ResolutionContext.

    The pipeline guarantees deterministic ordering.
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
        return f"{len(self.stages)} Resolution Stages"

    @property
    def display_description(self) -> str:
        return (
            "Ordered orchestration pipeline for Sanskrit "
            "linguistic resolution."
        )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        return len(self.stages)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def has_stages(self) -> bool:
        return not self.is_empty

    # ---------------------------------------------------------
    # Pipeline execution
    # ---------------------------------------------------------

    def execute(
        self,
        context: ResolutionContext,
    ) -> ResolutionContext:
        """
        Execute every stage sequentially.

        Each stage returns the updated ResolutionContext.

        Parameters
        ----------
        context:
            Initial resolution context.

        Returns
        -------
        ResolutionContext
            Fully enriched context after all stages have
            completed.
        """

        current_context = context

        for stage in self.stages:
            current_context = stage.execute(
                current_context,
            )

        return current_context

    # ---------------------------------------------------------
    # Immutable helpers
    # ---------------------------------------------------------

    def append(
        self,
        stage: ResolutionStage,
    ) -> "ResolutionPipeline":
        """
        Return a new pipeline with one additional stage.
        """

        return ResolutionPipeline(
            stages=self.stages + (stage,),
        )

    def extend(
        self,
        stages: tuple[
            ResolutionStage,
            ...
        ],
    ) -> "ResolutionPipeline":
        """
        Return a new pipeline with multiple stages appended.
        """

        return ResolutionPipeline(
            stages=self.stages + stages,
        )

    # ---------------------------------------------------------
    # Container protocol
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

    def __str__(
        self,
    ) -> str:
        return self.display_text
