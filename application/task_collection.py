from __future__ import annotations

"""
SanskritAI
==========

Task Collection

Defines the immutable collection of application Tasks.

A TaskCollection represents a semantic set of unique Tasks.
It intentionally preserves no execution order.

Execution ordering belongs to Workflow and Pipeline.

Architecture
------------

Task
    │
    ▼
TaskCollection
    │
    ├──────────────┐
    ▼              ▼
Workflow      PipelineStage

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.application.task import Task
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class TaskCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of unique Tasks.
    """

    tasks: frozenset[Task] = field(
        default_factory=frozenset,
    )

    @property
    def identifier(self) -> str:
        return "task_collection"

    @property
    def display_name(self) -> str:
        return "Task Collection"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name} "
            f"({len(self.tasks)} tasks)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable collection of unique application tasks."
        )

    @property
    def is_empty(self) -> bool:
        """
        Indicates whether the collection contains no tasks.
        """
        return not self.tasks

    @property
    def size(self) -> int:
        """
        Number of tasks.
        """
        return len(self.tasks)

    def contains(
        self,
        task: Task,
    ) -> bool:
        """
        Determines whether the supplied task exists in the
        collection.
        """
        return task in self.tasks

    def add(
        self,
        task: Task,
    ) -> "TaskCollection":
        """
        Returns a new collection containing the supplied task.
        """
        return TaskCollection(
            tasks=self.tasks | {task},
        )

    def remove(
        self,
        task: Task,
    ) -> "TaskCollection":
        """
        Returns a new collection without the supplied task.
        """
        return TaskCollection(
            tasks=self.tasks - {task},
        )

    def union(
        self,
        other: "TaskCollection",
    ) -> "TaskCollection":
        """
        Returns the union of two task collections.
        """
        return TaskCollection(
            tasks=self.tasks | other.tasks,
        )

    def intersection(
        self,
        other: "TaskCollection",
    ) -> "TaskCollection":
        """
        Returns the intersection of two task collections.
        """
        return TaskCollection(
            tasks=self.tasks & other.tasks,
        )

    def difference(
        self,
        other: "TaskCollection",
    ) -> "TaskCollection":
        """
        Returns the difference of two task collections.
        """
        return TaskCollection(
            tasks=self.tasks - other.tasks,
        )

    def __contains__(
        self,
        task: Task,
    ) -> bool:
        return task in self.tasks

    def __iter__(self) -> Iterator[Task]:
        return iter(self.tasks)

    def __len__(self) -> int:
        return len(self.tasks)

    def __str__(self) -> str:
        return self.display_text
