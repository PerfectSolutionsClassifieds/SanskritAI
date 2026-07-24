from __future__ import annotations

"""
SanskritAI
==========

Execution Plan

Defines the immutable compiled execution plan derived from a
Pipeline.

An ExecutionPlan represents the validated executable structure
that the Orchestrator executes.

The Pipeline remains the declarative definition, while the
ExecutionPlan is its compiled runtime representation.

Architecture
------------

Pipeline
    │
    ▼
ExecutionPlan
    │
    ▼
ExecutionContext

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.application.pipeline import Pipeline
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ExecutionPlan(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable execution plan.
    """

    pipeline: Pipeline

    validated: bool = True

    @property
    def identifier(self) -> str:
        return self.pipeline.identifier

    @property
    def display_name(self) -> str:
        return f"{self.pipeline.display_name} Plan"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Immutable compiled execution plan."
        )

    @property
    def stage_count(self) -> int:
        return self.pipeline.stage_count

    @property
    def workflow_count(self) -> int:
        return self.pipeline.workflow_count

    @property
    def step_count(self) -> int:
        return self.pipeline.step_count

    @property
    def task_count(self) -> int:
        return self.pipeline.task_count

    def __str__(self) -> str:
        return self.display_text
