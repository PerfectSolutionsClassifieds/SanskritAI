from __future__ import annotations

"""
SanskritAI
==========

Default Knowledge Graph Pipeline

Canonical pipeline responsible for orchestrating the complete
Knowledge Graph Kernel workflow.

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.pipeline.pipeline import Pipeline
from SanskritAI.core.pipeline.pipeline_context import PipelineContext
from SanskritAI.core.pipeline.pipeline_result import PipelineResult
from SanskritAI.core.pipeline.pipeline_step import PipelineStep

from SanskritAI.domain.knowledge_graph.knowledge_graph_context import (
    KnowledgeGraphContext,
)
from SanskritAI.domain.knowledge_graph.knowledge_graph_result import (
    KnowledgeGraphResult,
)


@dataclass(slots=True)
class DefaultKnowledgeGraphPipeline(Pipeline):
    """
    Canonical Knowledge Graph Pipeline.
    """

    name: str = "Default Knowledge Graph Pipeline"

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
            "Knowledge Graph Kernel."
        )

    # ---------------------------------------------------------

    def before_execute(
        self,
        context: PipelineContext,
    ) -> None:

        if not isinstance(
            context,
            KnowledgeGraphContext,
        ):
            raise TypeError(
                "DefaultKnowledgeGraphPipeline requires "
                "KnowledgeGraphContext."
            )

    def after_execute(
        self,
        context: PipelineContext,
        result: PipelineResult,
    ) -> KnowledgeGraphResult:

        return KnowledgeGraphResult(
            context=context,
            graph=result.output,
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

    def execute_graph(
        self,
        context: KnowledgeGraphContext,
    ) -> KnowledgeGraphResult:

        return self.execute(context)
