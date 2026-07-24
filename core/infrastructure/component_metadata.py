from __future__ import annotations

"""
SanskritAI
==========

Component Metadata

Defines the immutable semantic metadata describing an
infrastructure component.

ComponentMetadata owns only descriptive information.
Executable behavior belongs to Component and its subclasses.

Architecture
------------

Lifecycle
      │
      ▼
ComponentMetadata
      │
      ▼
Component

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.infrastructure.lifecycle import Lifecycle
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ComponentMetadata(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable metadata describing a runtime component.
    """

    identifier: str

    name: str

    lifecycle: Lifecycle

    description: str = ""

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return (
            f"{self.name} "
            f"({self.lifecycle.display_name})"
        )

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def is_active(self) -> bool:
        return self.lifecycle.is_active

    @property
    def is_terminal(self) -> bool:
        return self.lifecycle.is_terminal

    def __str__(self) -> str:
        return self.display_text
