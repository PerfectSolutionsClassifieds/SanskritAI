from __future__ import annotations

"""
SanskritAI
==========

Work Context

Defines the immutable execution context for a single unit of
application work.

A WorkContext bridges the Application Layer and the Core
Platform by providing access to the shared RuntimeContext
while remaining specific to one executable work item.

WorkContext intentionally contains no mutable execution state.
Runtime progress, cancellation, diagnostics, and results belong
to ExecutionContext.

Architecture
------------

RuntimeContext
        │
        ▼
WorkContext
        │
        ▼
Work
        │
        ▼
Task

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.infrastructure.runtime_context import RuntimeContext
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class WorkContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable execution context for a single unit of work.
    """

    runtime: RuntimeContext

    identifier: str = "work_context"

    description: str = ""

    @property
    def display_name(self) -> str:
        return "Work Context"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            self.description
            or "Immutable execution context for application work."
        )

    @property
    def configuration(self):
        """
        Shared configuration registry.
        """
        return self.runtime.configuration

    @property
    def services(self):
        """
        Shared service container.
        """
        return self.runtime.services

    @property
    def capabilities(self):
        """
        Shared capability registry.
        """
        return self.runtime.capabilities

    @property
    def plugins(self):
        """
        Shared plugin registry.
        """
        return self.runtime.plugins

    @property
    def resources(self):
        """
        Shared resource registry.
        """
        return self.runtime.resources

    @property
    def events(self):
        """
        Shared event dispatcher.
        """
        return self.runtime.events

    def __str__(self) -> str:
        return self.display_text
