from __future__ import annotations

"""
SanskritAI
==========

Universal Kernel Pipeline

The Universal Kernel Pipeline is the highest-level orchestration
pipeline within SanskritAI.

It composes the individual kernel pipelines into one reusable
processing workflow, allowing a single input śloka, sentence,
or lexical unit to traverse the complete SanskritAI linguistic
analysis stack.

Canonical execution order
-------------------------

    Derivation
        ↓
    Vakya
        ↓
    Semantic
        ↓
    Chandas
        ↓
    Alankara
        ↓
    Knowledge Graph

Each kernel remains completely independent while the Universal
Kernel Pipeline coordinates execution and aggregates the outputs.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.core.pipeline.pipeline import Pipeline
from SanskritAI.core.pipeline.pipeline_context import PipelineContext
from SanskritAI.core.pipeline.pipeline_result import PipelineResult
from SanskritAI.core.pipeline.pipeline_trace import PipelineTrace


@dataclass(slots=True)
class UniversalKernelPipeline(
    Displayable,
):
    """
    Canonical orchestrator for every SanskritAI kernel.
    """

    pipelines: tuple[
        Pipeline,
        ...
    ] = field(
        default_factory=tuple,
    )

    name: str = "Universal Kernel Pipeline"

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return self.name

    @property
    def display_text(
        self,
    ) -> str:
        return (
            f"{self.display_name}"
            f" ({self.pipeline_count} kernels)"
        )

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Composable orchestration pipeline for all "
            "SanskritAI linguistic kernels."
        )

    # ---------------------------------------------------------
    # Inspection
    # ---------------------------------------------------------

    @property
    def pipeline_count(
        self,
    ) -> int:
        return len(
            self.pipelines
        )

    @property
    def kernel_names(
        self,
    ) -> tuple[str, ...]:
        return tuple(
            pipeline.display_name
            for pipeline in self.pipelines
        )

    @property
    def is_empty(
        self,
    ) -> bool:
        return self.pipeline_count == 0

    @property
    def is_not_empty(
        self,
    ) -> bool:
        return not self.is_empty

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> tuple[
        PipelineResult,
        ...
    ]:
        """
        Executes every registered kernel pipeline in
        canonical order.

        The same context is forwarded through each kernel.

        Future versions may evolve the context after each
        stage, allowing downstream kernels to consume the
        previous kernel's output.
        """

        results: list[
            PipelineResult
        ] = []

        current_context = context

        for pipeline in self.pipelines:

            result = pipeline.execute(
                current_context
            )

            results.append(
                result
            )

        return tuple(
            results
        )

    # ---------------------------------------------------------
    # Aggregate execution
    # ---------------------------------------------------------

    def execute_with_trace(
        self,
        context: PipelineContext,
    ) -> tuple[
        tuple[PipelineResult, ...],
        PipelineTrace,
    ]:
        """
        Executes the entire kernel stack and merges
        pipeline traces into a single trace object.
        """

        results = self.execute(
            context
        )

        trace = PipelineTrace()

        for result in results:

            if hasattr(
                result,
                "trace",
            ):
                pipeline_trace = getattr(
                    result,
                    "trace",
                )

                if pipeline_trace is not None:

                    for step in pipeline_trace:

                        trace = trace.add(
                            step
                        )

        return (
            results,
            trace,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def append(
        self,
        pipeline: Pipeline,
    ) -> "UniversalKernelPipeline":
        """
        Returns a new pipeline with one additional kernel.
        """

        return UniversalKernelPipeline(
            pipelines=(
                *self.pipelines,
                pipeline,
            )
        )

    def __iter__(
        self,
    ):
        return iter(
            self.pipelines
        )

    def __len__(
        self,
    ) -> int:
        return self.pipeline_count

    def __str__(
        self,
    ) -> str:
        return self.display_text
