from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from SanskritAI.application.execution_plan import ExecutionPlan
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

    plan: ExecutionPlan

    execution_id: UUID = field(default_factory=uuid4)

    started_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def identifier(self) -> str:
        return str(self.execution_id)

    @property
    def pipeline(self):
        """
        Convenience access to the originating Pipeline.
        """
        return self.plan.pipeline

    @property
    def display_name(self) -> str:
        return "Execution Context"

    @property
    def display_text(self) -> str:
        return f"{self.pipeline.display_name} Execution"

    @property
    def display_description(self) -> str:
        return "Immutable execution session."

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
