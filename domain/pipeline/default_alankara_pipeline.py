from __future__ import annotations

"""
SanskritAI
==========

Default Alankara Pipeline

Canonical pipeline responsible for orchestrating the complete
Alaṅkāra Kernel workflow.

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.pipeline.pipeline import Pipeline
from SanskritAI.core.pipeline.pipeline_context import PipelineContext
from SanskritAI.core.pipeline.pipeline_result import PipelineResult
from SanskritAI.core.pipeline.pipeline_step import PipelineStep

from SanskritAI.domain.alankara.alankara_context import (
    AlankaraContext,
)
from SanskritAI.domain.alankara.alankara_result import (
    AlankaraResult,
)


@dataclass(slots=True)
class DefaultAlankaraPipeline(Pipeline):
    """
    Canonical Alaṅkāra Pipeline.
    """

    name: str = "Default Alankara Pipeline"

    steps: tuple[
        PipelineStep,
        ...
    ] = field(
        default_factory=tuple,
    )

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
            "Alankara Kernel."
        )

    # ---------------------------------------------------------

    def before_execute(
        self,
        context: PipelineContext,
    ) -> None:

        if not isinstance(
            context,
            AlankaraContext,
        ):
            raise TypeError(
                "DefaultAlankaraPipeline requires "
                "AlankaraContext."
            )

    def after_execute(
        self,
        context: PipelineContext,
        result: PipelineResult,
    ) -> AlankaraResult:

        return AlankaraResult(
            context=context,
            analyses=result.output,
            succeeded=result.succeeded,
            confidence=result.confidence,
            diagnostics=result.diagnostics,
        )

    # ---------------------------------------------------------

    @property
    def step_names(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            step.display_name
            for step in self.ordered_steps
        )

    @property
    def is_configured(
        self,
    ) -> bool:
        return not self.is_empty

    def execute_alankara(
        self,
        context: AlankaraContext,
    ) -> AlankaraResult:

        return self.execute(context)
