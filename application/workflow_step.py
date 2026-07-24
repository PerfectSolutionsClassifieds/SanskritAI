from __future__ import annotations

"""
SanskritAI
==========

Workflow Step

Defines the immutable building block of a Workflow.

A WorkflowStep groups one or more Tasks into a logical
execution step. It contains no execution behavior.

Execution is performed by the Orchestrator.

Architecture
------------

TaskCollection
        │
        ▼
WorkflowStep
        │
        ▼
Workflow

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.application.task_collection import TaskCollection
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class WorkflowStep(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable workflow step.
    """

    identifier: str

    tasks: TaskCollection

    name: str

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
        Indicates whether this workflow step contains no tasks.
        """
        return self.tasks.is_empty

    @property
    def task_count(self) -> int:
        """
        Number of tasks in this workflow step.
        """
        return self.tasks.size

    def contains(self, task) -> bool:
        """
        Determines whether the supplied task belongs to this step.
        """
        return task in self.tasks

    def __str__(self) -> str:
        return self.display_text
