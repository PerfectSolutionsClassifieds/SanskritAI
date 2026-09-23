from __future__ import annotations

"""
SanskritAI
==========

Execution Context

Defines the immutable runtime execution context for a single
Pipeline execution.

ExecutionContext bridges the declarative Application Layer
and the runtime Orchestrator.

ExecutionContext owns execution-specific state but contains
no execution behavior.

Architecture
------------

Pipeline
    │
    ▼
ExecutionContext
    │
    ▼
ExecutionResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from SanskritAI.application.pipeline import Pipeline
from SanskritAI.core.infrastructure.runtime_context import RuntimeContext
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ExecutionContext(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable execution context.
    """

    runtime: RuntimeContext

    pipeline: Pipeline

    execution_id: UUID = field(
        default_factory=uuid4,
    )

    started_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    @property
    def identifier(self) -> str:
        return str(self.execution_id)

    @property
    def display_name(self) -> str:
        return "Execution Context"

    @property
    def display_text(self) -> str:
        return (
            f"{self.pipeline.display_name}"
            f" Execution"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable execution session."
        )

    @property
    def configuration(self):
        return self.runtime.configuration

    @property
    def services(self):
        return self.runtime.services

    @property
    def plugins(self):
        return self.runtime.plugins

    @property
    def resources(self):
        return self.runtime.resources

    @property
    def events(self):
        return self.runtime.events

    def __str__(self) -> str:
        return self.display_text
