from __future__ import annotations

"""
SanskritAI
==========

Pipeline

Defines the immutable top-level executable application
pipeline.

A Pipeline is composed of one or more ordered PipelineStage
objects and represents an entire declarative application
workflow.

A Pipeline contains no execution behavior.

Execution belongs to the Orchestrator.

Architecture
------------

PipelineStage
        │
        ▼
Pipeline
        │
        ▼
ExecutionContext
        │
        ▼
Orchestrator

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.application.pipeline_stage import PipelineStage
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Pipeline(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable application pipeline.
    """

    identifier: str

    name: str

    stages: tuple[PipelineStage, ...] = field(
        default_factory=tuple,
    )

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def is_empty(self) -> bool:
        """
        Indicates whether this pipeline contains no stages.
        """
        return len(self.stages) == 0

    @property
    def stage_count(self) -> int:
        """
        Number of pipeline stages.
        """
        return len(self.stages)

    @property
    def workflow_count(self) -> int:
        """
        Total number of workflows.
        """
        return sum(
            stage.workflow_count
            for stage in self.stages
        )

    @property
    def step_count(self) -> int:
        """
        Total number of workflow steps.
        """
        return sum(
            stage.step_count
            for stage in self.stages
        )

    @property
    def task_count(self) -> int:
        """
        Total number of tasks.
        """
        return sum(
            stage.task_count
            for stage in self.stages
        )

    def add_stage(
        self,
        stage: PipelineStage,
    ) -> "Pipeline":
        """
        Returns a new Pipeline with an appended stage.
        """
        return Pipeline(
            identifier=self.identifier,
            name=self.name,
            stages=self.stages + (stage,),
            description=self.description,
        )

    def __iter__(self) -> Iterator[PipelineStage]:
        return iter(self.stages)

    def __len__(self) -> int:
        return len(self.stages)

    def __str__(self) -> str:
        return self.display_text
