from __future__ import annotations

"""
SanskritAI
==========

Component

Defines the immutable base class for runtime infrastructure
components.

A Component composes ComponentMetadata and serves as the
foundation for executable infrastructure services.

Architecture
------------

ComponentMetadata
        │
        ▼
Component
        │
        ▼
InfrastructureService

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.infrastructure.component_metadata import (
    ComponentMetadata,
)
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Component(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable runtime component.
    """

    metadata: ComponentMetadata

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
    def lifecycle(self):
        return self.metadata.lifecycle

    @property
    def is_active(self) -> bool:
        return self.metadata.is_active

    @property
    def is_terminal(self) -> bool:
        return self.metadata.is_terminal

    def __str__(self) -> str:
        return self.display_text
