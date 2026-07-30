from __future__ import annotations

"""
SanskritAI
==========

Default Vakya Pipeline

Canonical pipeline responsible for orchestrating the complete
Vākya (Sentence Analysis) Kernel workflow.

Execution mechanics are inherited entirely from the reusable
Core Pipeline framework.

Architecture
------------

PipelineContext
        │
        ▼
DefaultVakyaPipeline
        │
        ▼
Vakya Parser
        │
        ▼
Vakya Rule Set
        │
        ▼
Vakya Strategy
        │
        ▼
Vakya Result

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.pipeline.pipeline import Pipeline
from SanskritAI.core.pipeline.pipeline_context import PipelineContext
from SanskritAI.core.pipeline.pipeline_result import PipelineResult
from SanskritAI.core.pipeline.pipeline_step import PipelineStep

from SanskritAI.domain.vakya.vakya_context import (
    VakyaContext,
)
from SanskritAI.domain.vakya.vakya_result import (
    VakyaResult,
)


@dataclass(slots=True)
class DefaultVakyaPipeline(Pipeline):
    """
    Canonical Vākya Pipeline.

    The reusable Core Pipeline performs execution,
    tracing, diagnostics, ordering and confidence
    propagation.

    This class contributes only Vākya-specific
    validation and result wrapping.
    """

    name: str = "Default Vakya Pipeline"

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
            "Vākya Kernel."
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
            VakyaContext,
        ):
            raise TypeError(
                "DefaultVakyaPipeline requires "
                "VakyaContext."
            )

    def after_execute(
        self,
        context: PipelineContext,
        result: PipelineResult,
    ) -> VakyaResult:
        """
        Wraps the generic PipelineResult inside the
        canonical VakyaResult.
        """

        return VakyaResult(
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
        Returns ordered pipeline step names.
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
        Returns True if one or more pipeline
        steps have been configured.
        """
        return not self.is_empty

    def execute_vakya(
        self,
        context: VakyaContext,
    ) -> VakyaResult:
        """
        Domain-friendly execution alias.
        """
        return self.execute(context)
