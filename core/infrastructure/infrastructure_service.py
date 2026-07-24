from __future__ import annotations

"""
SanskritAI
==========

Infrastructure Service

Defines the canonical runtime infrastructure service.

An InfrastructureService composes a Component and serves as
the foundation for executable runtime services.

Concrete runtime services include:

- EventBus
- PluginManager
- ResourceLoader
- Cache
- Pipeline

Architecture
------------

Component
      │
      ▼
InfrastructureService
      │
      ▼
LifecycleManager

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.infrastructure.component import Component
from SanskritAI.core.infrastructure.component_metadata import ComponentMetadata
from SanskritAI.core.infrastructure.lifecycle import Lifecycle
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class InfrastructureService(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable infrastructure service.
    """

    component: Component

    @property
    def identifier(self) -> str:
        return self.component.identifier

    @property
    def display_name(self) -> str:
        return self.component.display_name

    @property
    def display_text(self) -> str:
        return self.component.display_text

    @property
    def display_description(self) -> str:
        return self.component.display_description

    @property
    def lifecycle(self) -> Lifecycle:
        return self.component.lifecycle

    @property
    def is_active(self) -> bool:
        return self.component.is_active

    @property
    def is_terminal(self) -> bool:
        return self.component.is_terminal

    def with_lifecycle(
        self,
        lifecycle: Lifecycle,
    ) -> "InfrastructureService":
        """
        Returns a new InfrastructureService with the
        supplied lifecycle.
        """

        metadata = ComponentMetadata(
            identifier=self.component.metadata.identifier,
            name=self.component.metadata.name,
            lifecycle=lifecycle,
            description=self.component.metadata.description,
        )

        component = Component(
            metadata=metadata,
        )

        return InfrastructureService(
            component=component,
        )

    def __str__(self) -> str:
        return self.display_text
