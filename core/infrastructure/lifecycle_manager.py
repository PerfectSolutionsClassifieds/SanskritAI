from __future__ import annotations

"""
SanskritAI
==========

Lifecycle Manager

Defines the immutable lifecycle transition manager.

LifecycleManager performs deterministic lifecycle transitions
without owning mutable runtime state.

Architecture
------------

InfrastructureService
        │
        ▼
LifecycleManager
        │
        ▼
EventEnvelope
(Infrastructure)

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.infrastructure.infrastructure_service import (
    InfrastructureService,
)
from SanskritAI.core.infrastructure.lifecycle import Lifecycle
from SanskritAI.core.infrastructure.runtime_state import RuntimeState
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class LifecycleManager(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable lifecycle transition manager.
    """

    @property
    def identifier(self) -> str:
        return "lifecycle_manager"

    @property
    def display_name(self) -> str:
        return "Lifecycle Manager"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Deterministically manages lifecycle "
            "state transitions."
        )

    def transition(
        self,
        service: InfrastructureService,
        state: RuntimeState,
    ) -> InfrastructureService:
        """
        Returns a new InfrastructureService whose
        component has transitioned to the supplied state.
        """

        new_lifecycle = service.lifecycle.transition_to(
            state,
        )

        new_metadata = service.component.metadata.__class__(
            identifier=service.component.metadata.identifier,
            name=service.component.metadata.name,
            lifecycle=new_lifecycle,
            description=service.component.metadata.description,
        )

        new_component = service.component.__class__(
            metadata=new_metadata,
        )

        return InfrastructureService(
            component=new_component,
        )

    def __str__(self) -> str:
        return self.display_text
