from __future__ import annotations

"""
SanskritAI
==========

Default Chandas Pipeline

Canonical pipeline responsible for orchestrating the complete
Chandas (Prosody / Metre) Kernel workflow.

Execution mechanics are inherited entirely from the reusable
Core Pipeline framework.

Architecture
------------

PipelineContext
        │
        ▼
DefaultChandasPipeline
        │
        ▼
Chandas Normalizer
        │
        ▼
Chandas Rule Set
        │
        ▼
Chandas Strategy
        │
        ▼
Chandas Result

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.pipeline.pipeline import Pipeline
from SanskritAI.core.pipeline.pipeline_context import PipelineContext
from SanskritAI.core.pipeline.pipeline_result import PipelineResult
from SanskritAI.core.pipeline.pipeline_step import PipelineStep

from SanskritAI.domain.chandas.chandas_context import (
    ChandasContext,
)
from SanskritAI.domain.chandas.chandas_result import (
    ChandasResult,
)


@dataclass(slots=True)
class DefaultChandasPipeline(Pipeline):
    """
    Canonical Chandas Pipeline.

    The reusable Core Pipeline performs execution,
    tracing, diagnostics, ordering and confidence
    propagation.

    This class contributes only Chandas-specific
    validation and result wrapping.
    """

    name: str = "Default Chandas Pipeline"

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
            "Chandas Kernel."
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
            ChandasContext,
        ):
            raise TypeError(
                "DefaultChandasPipeline requires "
                "ChandasContext."
            )

    def after_execute(
        self,
        context: PipelineContext,
        result: PipelineResult,
    ) -> ChandasResult:
        """
        Wraps the generic PipelineResult inside the
        canonical ChandasResult.
        """

        return ChandasResult(
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
        Returns True if one or more pipeline
        steps have been configured.
        """
        return not self.is_empty

    def execute_chandas(
        self,
        context: ChandasContext,
    ) -> ChandasResult:
        """
        Domain-friendly execution alias.
        """
        return self.execute(context)
