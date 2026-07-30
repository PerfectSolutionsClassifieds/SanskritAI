from __future__ import annotations

"""
SanskritAI
==========

Execution Result

Defines the immutable outcome of executing an ExecutionContext.

ExecutionResult represents the complete outcome of one
execution session.

Architecture
------------

ExecutionContext
      │
      ▼
ExecutionResult
      │
      ▼
Orchestrator

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.application.execution_context import ExecutionContext
from SanskritAI.application.execution_plan import ExecutionPlan
from SanskritAI.application.pipeline import Pipeline
from SanskritAI.application.task_result_collection import (
    TaskResultCollection,
)
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ExecutionResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable execution result.
    """

    context: ExecutionContext

    results: TaskResultCollection

    succeeded: bool

    message: str = ""

    @property
    def identifier(self) -> str:
        return self.context.identifier

    @property
    def plan(self) -> ExecutionPlan:
        """
        Convenience access to the originating execution plan.
        """
        return self.context.plan

    @property
    def pipeline(self) -> Pipeline:
        """
        Convenience access to the originating pipeline.
        """
        return self.context.pipeline

    @property
    def display_name(self) -> str:
        return f"{self.pipeline.display_name} Result"

    @property
    def display_text(self) -> str:
        status = "Succeeded" if self.succeeded else "Failed"
        return f"{self.pipeline.display_name} [{status}]"

    @property
    def display_description(self) -> str:
        return self.message

    @property
    def is_success(self) -> bool:
        return self.succeeded

    @property
    def is_failure(self) -> bool:
        return not self.succeeded

    @property
    def success_count(self) -> int:
        return self.results.success_count

    @property
    def failure_count(self) -> int:
        return self.results.failure_count

    @property
    def has_failures(self) -> bool:
        return self.results.any_failed

    @property
    def task_count(self) -> int:
        return len(self.results)

    @property
    def has_results(self) -> bool:
        return not self.results.is_empty

    def __str__(self) -> str:
        return self.display_text
