from __future__ import annotations

"""
SanskritAI
==========

Default Derivation Pipeline

Canonical pipeline responsible for orchestrating the complete
morphological derivation workflow.

Unlike earlier versions, this implementation delegates all
execution mechanics to the reusable Core Pipeline framework.

Architecture
------------

PipelineContext
        │
        ▼
DefaultDerivationPipeline
        │
        ▼
Paninian Rule Engine
        │
        ▼
Derivation Strategy
        │
        ▼
Derivation Result

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.pipeline.pipeline import Pipeline
from SanskritAI.core.pipeline.pipeline_context import PipelineContext
from SanskritAI.core.pipeline.pipeline_result import PipelineResult
from SanskritAI.core.pipeline.pipeline_step import PipelineStep

from SanskritAI.domain.pipeline.derivation_pipeline_context import (
    DerivationPipelineContext,
)
from SanskritAI.domain.pipeline.derivation_pipeline_result import (
    DerivationPipelineResult,
)


@dataclass(slots=True)
class DefaultDerivationPipeline(Pipeline):
    """
    Canonical Derivation Pipeline.

    This class is intentionally lightweight.

    Execution is inherited entirely from
    SanskritAI.core.pipeline.Pipeline.
    """

    name: str = "Default Derivation Pipeline"

    steps: tuple[
        PipelineStep,
        ...
    ] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical pipeline for morphological "
            "derivation."
        )

    # ---------------------------------------------------------
    # Hooks
    # ---------------------------------------------------------

    def before_execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Performs lightweight validation before pipeline
        execution.
        """

        if not isinstance(
            context,
            DerivationPipelineContext,
        ):
            raise TypeError(
                "DefaultDerivationPipeline requires "
                "DerivationPipelineContext."
            )

    def after_execute(
        self,
        context: PipelineContext,
        result: PipelineResult,
    ) -> DerivationPipelineResult:
        """
        Wraps the generic PipelineResult inside the domain
        specific DerivationPipelineResult.
        """

        return DerivationPipelineResult(
            context=context,
            trace=result.trace,
            output=result.output,
            succeeded=result.succeeded,
            confidence=result.confidence,
            diagnostics=result.diagnostics,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def step_names(
        self,
    ) -> tuple[str, ...]:
        """
        Returns the ordered pipeline step names.
        """
        return tuple(
            step.display_name
            for step in self.ordered_steps
        )

    @property
    def is_configured(
        self,
    ) -> bool:
        """
        True if at least one step has been configured.
        """
        return not self.is_empty

    def execute_derivation(
        self,
        context: DerivationPipelineContext,
    ) -> DerivationPipelineResult:
        """
        Domain-friendly alias for execute().
        """
        return self.execute(context)
