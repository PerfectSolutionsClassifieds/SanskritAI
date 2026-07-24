from __future__ import annotations

"""
SanskritAI
==========

Task

Defines the canonical immutable atomic executable work unit.

A Task represents an atomic unit of application work.
It composes TaskMetadata and WorkContext while remaining
entirely declarative.

Tasks contain no execution logic.

Execution belongs to the Orchestrator.

Architecture
------------

TaskMetadata
      │
WorkContext
      │
      ▼
Task
      │
      ▼
WorkflowStep

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.application.task_metadata import TaskMetadata
from SanskritAI.application.work import Work
from SanskritAI.application.work_context import WorkContext
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable


@dataclass(frozen=True, slots=True)
class Task(
    Work,
    Immutable,
    Displayable,
):
    """
    Immutable atomic application task.
    """

    metadata: TaskMetadata

    context: WorkContext

    @property
    def identifier(self) -> str:
        return self.metadata.identifier

    @property
    def display_name(self) -> str:
        return self.metadata.display_name

    @property
    def display_text(self) -> str:
        return self.metadata.display_text

    @property
    def display_description(self) -> str:
        return self.metadata.display_description

    @property
    def version(self):
        """
        Task version.
        """
        return self.metadata.version

    @property
    def capabilities(self):
        """
        Declared task capabilities.
        """
        return self.metadata.capabilities

    @property
    def runtime(self):
        """
        Shared runtime context.
        """
        return self.context.runtime

    @property
    def configuration(self):
        return self.context.configuration

    @property
    def services(self):
        return self.context.services

    @property
    def plugins(self):
        return self.context.plugins

    @property
    def resources(self):
        return self.context.resources

    @property
    def events(self):
        return self.context.events

    @property
    def is_atomic(self) -> bool:
        return self.metadata.atomic

    @property
    def is_interruptible(self) -> bool:
        return self.metadata.interruptible

    @property
    def is_retryable(self) -> bool:
        return self.metadata.retryable

    def __str__(self) -> str:
        return self.display_text
