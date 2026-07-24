from __future__ import annotations

"""
SanskritAI
==========

Pipeline Stage

Defines an immutable PipelineStage composed of one or more
Workflows.

A PipelineStage represents a logical phase within a Pipeline.
It is declarative and contains no execution behavior.

Execution belongs to the Orchestrator.

Architecture
------------

Workflow
      │
      ▼
PipelineStage
      │
      ▼
Pipeline

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.application.workflow import Workflow
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PipelineStage(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable pipeline stage.
    """

    identifier: str

    name: str

    workflows: tuple[Workflow, ...] = field(
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
        Indicates whether this stage contains no workflows.
        """
        return len(self.workflows) == 0

    @property
    def workflow_count(self) -> int:
        """
        Number of workflows in this stage.
        """
        return len(self.workflows)

    @property
    def step_count(self) -> int:
        """
        Total number of workflow steps.
        """
        return sum(
            workflow.step_count
            for workflow in self.workflows
        )

    @property
    def task_count(self) -> int:
        """
        Total number of tasks.
        """
        return sum(
            workflow.task_count
            for workflow in self.workflows
        )

    def add_workflow(
        self,
        workflow: Workflow,
    ) -> "PipelineStage":
        """
        Returns a new PipelineStage with an appended workflow.
        """
        return PipelineStage(
            identifier=self.identifier,
            name=self.name,
            workflows=self.workflows + (workflow,),
            description=self.description,
        )

    def __iter__(self) -> Iterator[Workflow]:
        return iter(self.workflows)

    def __len__(self) -> int:
        return len(self.workflows)

    def __str__(self) -> str:
        return self.display_text
