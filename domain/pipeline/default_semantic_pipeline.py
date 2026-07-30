from __future__ import annotations

"""
SanskritAI
==========

Default Semantic Pipeline

Canonical pipeline responsible for orchestrating the complete
Semantic Kernel workflow.

Execution mechanics are inherited entirely from the reusable
Core Pipeline framework.

Architecture
------------

PipelineContext
        │
        ▼
DefaultSemanticPipeline
        │
        ▼
Semantic Rules
        │
        ▼
Semantic Strategy
        │
        ▼
Semantic Result

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.pipeline.pipeline import Pipeline
from SanskritAI.core.pipeline.pipeline_context import PipelineContext
from SanskritAI.core.pipeline.pipeline_result import PipelineResult
from SanskritAI.core.pipeline.pipeline_step import PipelineStep

from SanskritAI.domain.semantic.semantic_context import (
    SemanticContext,
)
from SanskritAI.domain.semantic.semantic_result import (
    SemanticResult,
)


@dataclass(slots=True)
class DefaultSemanticPipeline(Pipeline):
    """
    Canonical Semantic Pipeline.

    The Core Pipeline performs all execution,
    tracing, diagnostics, ordering and confidence
    propagation.

    This class only contributes semantic-specific
    validation and result wrapping.
    """

    name: str = "Default Semantic Pipeline"

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
            "Canonical pipeline for the "
            "Semantic Kernel."
        )

    # ---------------------------------------------------------
    # Pipeline Hooks
    # ---------------------------------------------------------

    def before_execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Validates the incoming pipeline context.
        """

        if not isinstance(
            context,
            SemanticContext,
        ):
            raise TypeError(
                "DefaultSemanticPipeline requires "
                "SemanticContext."
            )

    def after_execute(
        self,
        context: PipelineContext,
        result: PipelineResult,
    ) -> SemanticResult:
        """
        Wraps the generic PipelineResult inside the
        canonical SemanticResult.
        """

        return SemanticResult(
            context=context,
            analyses=result.output,
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
        Ordered pipeline step names.
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
        Returns True when at least one step has been
        configured.
        """
        return not self.is_empty

    def execute_semantic(
        self,
        context: SemanticContext,
    ) -> SemanticResult:
        """
        Semantic-friendly execution alias.
        """
        return self.execute(context)
