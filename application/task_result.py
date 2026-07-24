from __future__ import annotations

"""
SanskritAI
==========

Task Result

Defines the immutable outcome of executing a single Task.

TaskResult separates execution outcomes from task definitions.
It contains no execution behavior and owns no mutable state.

Execution is performed by the Orchestrator.

Architecture
------------

Task
    │
    ▼
TaskResult
    │
    ▼
WorkflowStep

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.application.task import Task
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class TaskResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable outcome of executing a Task.
    """

    task: Task

    succeeded: bool

    output: Any | None = None

    message: str = ""

    diagnostics: frozenset[str] = field(
        default_factory=frozenset,
    )

    @property
    def identifier(self) -> str:
        """
        Uses the originating task identifier.
        """
        return self.task.identifier

    @property
    def display_name(self) -> str:
        return f"{self.task.display_name} Result"

    @property
    def display_text(self) -> str:
        status = "Succeeded" if self.succeeded else "Failed"
        return f"{self.task.display_name} [{status}]"

    @property
    def display_description(self) -> str:
        return self.message

    @property
    def is_success(self) -> bool:
        """
        Indicates successful execution.
        """
        return self.succeeded

    @property
    def is_failure(self) -> bool:
        """
        Indicates failed execution.
        """
        return not self.succeeded

    @property
    def has_output(self) -> bool:
        """
        Indicates whether the task produced an output.
        """
        return self.output is not None

    @property
    def has_diagnostics(self) -> bool:
        """
        Indicates whether diagnostic information exists.
        """
        return bool(self.diagnostics)

    def add_diagnostic(
        self,
        diagnostic: str,
    ) -> "TaskResult":
        """
        Returns a new TaskResult with an additional diagnostic.
        """
        return TaskResult(
            task=self.task,
            succeeded=self.succeeded,
            output=self.output,
            message=self.message,
            diagnostics=self.diagnostics | {diagnostic},
        )

    def __str__(self) -> str:
        return self.display_text
