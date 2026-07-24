from __future__ import annotations

"""
SanskritAI
==========

Workflow

Defines an immutable Workflow composed of one or more
WorkflowStep objects.

A Workflow is declarative. It describes execution structure
without executing it.

Execution belongs to the Orchestrator.

Architecture
------------

WorkflowStep
      │
      ▼
Workflow
      │
      ▼
PipelineStage

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.application.workflow_step import WorkflowStep
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Workflow(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable workflow.
    """

    identifier: str

    name: str

    steps: tuple[WorkflowStep, ...] = field(
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
        return len(self.steps) == 0

    @property
    def step_count(self) -> int:
        return len(self.steps)

    @property
    def task_count(self) -> int:
        return sum(
            step.task_count
            for step in self.steps
        )

    def add_step(
        self,
        step: WorkflowStep,
    ) -> "Workflow":
        """
        Returns a new workflow with an appended step.
        """
        return Workflow(
            identifier=self.identifier,
            name=self.name,
            steps=self.steps + (step,),
            description=self.description,
        )

    def __iter__(self) -> Iterator[WorkflowStep]:
        return iter(self.steps)

    def __len__(self) -> int:
        return len(self.steps)

    def __str__(self) -> str:
        return self.display_text
