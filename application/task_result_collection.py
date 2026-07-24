from __future__ import annotations

"""
SanskritAI
==========

Task Result Collection

Defines the immutable collection of TaskResult objects.

A TaskResultCollection represents a semantic set of unique
task execution outcomes.

Execution ordering intentionally does not belong here.
Ordering belongs to Workflow and Pipeline.

Architecture
------------

TaskResult
      │
      ▼
TaskResultCollection
      │
      ├──────────────┐
      ▼              ▼
WorkflowStep      Workflow

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.application.task_result import TaskResult
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class TaskResultCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of unique TaskResult objects.
    """

    results: frozenset[TaskResult] = field(
        default_factory=frozenset,
    )

    @property
    def identifier(self) -> str:
        return "task_result_collection"

    @property
    def display_name(self) -> str:
        return "Task Result Collection"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name} "
            f"({len(self.results)} results)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable collection of task execution results."
        )

    @property
    def is_empty(self) -> bool:
        """
        Indicates whether the collection is empty.
        """
        return not self.results

    @property
    def size(self) -> int:
        """
        Number of task results.
        """
        return len(self.results)

    @property
    def succeeded(self) -> frozenset[TaskResult]:
        """
        Returns all successful task results.
        """
        return frozenset(
            result
            for result in self.results
            if result.is_success
        )

    @property
    def failed(self) -> frozenset[TaskResult]:
        """
        Returns all failed task results.
        """
        return frozenset(
            result
            for result in self.results
            if result.is_failure
        )

    @property
    def success_count(self) -> int:
        return len(self.succeeded)

    @property
    def failure_count(self) -> int:
        return len(self.failed)

    @property
    def all_succeeded(self) -> bool:
        """
        Indicates whether every task succeeded.
        """
        return (
            bool(self.results)
            and self.failure_count == 0
        )

    @property
    def any_failed(self) -> bool:
        """
        Indicates whether any task failed.
        """
        return self.failure_count > 0

    def contains(
        self,
        result: TaskResult,
    ) -> bool:
        return result in self.results

    def add(
        self,
        result: TaskResult,
    ) -> "TaskResultCollection":
        """
        Returns a new collection containing the supplied
        task result.
        """
        return TaskResultCollection(
            results=self.results | {result},
        )

    def remove(
        self,
        result: TaskResult,
    ) -> "TaskResultCollection":
        """
        Returns a new collection without the supplied
        task result.
        """
        return TaskResultCollection(
            results=self.results - {result},
        )

    def union(
        self,
        other: "TaskResultCollection",
    ) -> "TaskResultCollection":
        return TaskResultCollection(
            results=self.results | other.results,
        )

    def intersection(
        self,
        other: "TaskResultCollection",
    ) -> "TaskResultCollection":
        return TaskResultCollection(
            results=self.results & other.results,
        )

    def difference(
        self,
        other: "TaskResultCollection",
    ) -> "TaskResultCollection":
        return TaskResultCollection(
            results=self.results - other.results,
        )

    def __contains__(
        self,
        result: TaskResult,
    ) -> bool:
        return result in self.results

    def __iter__(self) -> Iterator[TaskResult]:
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def __str__(self) -> str:
        return self.display_text
