from __future__ import annotations

"""
SanskritAI
==========

Core Pipeline

Reusable execution engine shared by every SanskritAI kernel.

This class is intentionally domain-independent.  Concrete
pipelines (Derivation, Semantic, Vakya, Chandas,
Alankara, Knowledge Graph, etc.) should inherit from this
class and supply only their PipelineSteps.

Execution Flow
--------------

PipelineContext
        │
        ▼
Pipeline.execute()
        │
        ▼
PipelineStep.execute()
        │
        ▼
PipelineTrace
        │
        ▼
PipelineResult

Version
-------
v1.0.0
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.collections.collection import Collection
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.core.pipeline.pipeline_context import (
    PipelineContext,
)
from SanskritAI.core.pipeline.pipeline_result import (
    PipelineResult,
)
from SanskritAI.core.pipeline.pipeline_step import (
    PipelineStep,
)
from SanskritAI.core.pipeline.pipeline_trace import (
    PipelineTrace,
    PipelineTraceEntry,
)


# ---------------------------------------------------------
# Pipeline
# ---------------------------------------------------------

@dataclass(slots=True)
class Pipeline(
    ABC,
    Immutable,
    Displayable,
):
    """
    Generic reusable execution pipeline.
    """

    steps: tuple[
        PipelineStep,
        ...
    ] = field(default_factory=tuple)

    name: str = "Pipeline"

    # -----------------------------------------------------
    # Display
    # -----------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Reusable execution pipeline."
        )

    # -----------------------------------------------------
    # Step helpers
    # -----------------------------------------------------

    @property
    def ordered_steps(
        self,
    ) -> tuple[
        PipelineStep,
        ...
    ]:
        """
        Returns the pipeline steps sorted by priority.
        """
        return tuple(
            sorted(
                self.steps,
                key=lambda step: (
                    step.priority,
                    step.identifier,
                ),
            )
        )

    @property
    def step_count(self) -> int:
        return len(self.steps)

    @property
    def is_empty(self) -> bool:
        return self.step_count == 0

    # -----------------------------------------------------
    # Mutation helpers
    # -----------------------------------------------------

    def add_step(
        self,
        step: PipelineStep,
    ) -> "Pipeline":
        """
        Returns a new pipeline with the additional step.
        """
        return type(self)(
            steps=self.steps + (step,),
            name=self.name,
        )

    # -----------------------------------------------------
    # Execution hooks
    # -----------------------------------------------------

    def before_execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Optional hook executed before the pipeline starts.
        """
        return None

    def after_execute(
        self,
        context: PipelineContext,
        result: PipelineResult,
    ) -> PipelineResult:
        """
        Optional hook executed after the pipeline completes.
        """
        return result

    # -----------------------------------------------------
    # Execution
    # -----------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineResult:
        """
        Executes the pipeline.

        Every step receives

            context
            previous_result

        and returns the next result.
        """

        self.before_execute(context)

        trace = PipelineTrace()

        previous_result: Any = None

        diagnostics: list[str] = []

        succeeded = True

        confidence = 1.0

        for order, step in enumerate(
            self.ordered_steps,
            start=1,
        ):

            try:

                output = step.execute(
                    context=context,
                    previous_result=previous_result,
                )

                entry = PipelineTraceEntry(
                    step=step,
                    input_value=previous_result,
                    output_value=output,
                    execution_order=order,
                    succeeded=True,
                    confidence=confidence,
                )

                trace = trace.add(entry)

                previous_result = output

            except Exception as exc:

                succeeded = False

                diagnostics.append(str(exc))

                entry = PipelineTraceEntry(
                    step=step,
                    input_value=previous_result,
                    output_value=None,
                    execution_order=order,
                    succeeded=False,
                    diagnostics=(str(exc),),
                    confidence=0.0,
                )

                trace = trace.add(entry)

                confidence = 0.0

                break

        result = PipelineResult(
            context=context,
            trace=trace,
            output=previous_result,
            succeeded=succeeded,
            confidence=confidence,
            diagnostics=tuple(diagnostics),
        )

        return self.after_execute(
            context=context,
            result=result,
        )

    # -----------------------------------------------------

    def __call__(
        self,
        context: PipelineContext,
    ) -> PipelineResult:
        """
        Enables

            pipeline(context)

        syntax.
        """
        return self.execute(context)

    def __str__(self) -> str:
        return self.display_text
