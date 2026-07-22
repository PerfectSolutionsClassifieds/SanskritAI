from __future__ import annotations

"""
SanskritAI
==========

Capability Profile

Defines the immutable capability profile advertised by a
component.

A CapabilityProfile associates a named component with the set of
capabilities that it provides.

Unlike CapabilityRegistry, which represents the universe of
known capabilities, a CapabilityProfile represents the
capabilities of a single component.

Typical examples include:

- Paninian Parser
- Amarakośa Dictionary
- Śabdakalpadruma
- Corpus Importer
- AI Embedding Backend
- Vector Search Engine

Architecture
------------

ValueObject
      │
      ▼
CapabilityProfile
      │
      ├── name
      └── CapabilitySet

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.capabilities.capability import Capability
from SanskritAI.core.capabilities.capability_set import CapabilitySet
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class CapabilityProfile(ValueObject, Immutable, Displayable):
    """
    Immutable capability profile of a component.
    """

    name: str

    capabilities: CapabilitySet

    description: str = ""

    def __post_init__(self) -> None:
        normalized = self.name.strip()

        if not normalized:
            raise ValueError(
                "Profile name cannot be empty."
            )

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """
        Canonical profile identifier.
        """
        return self.name

    def supports(
        self,
        capability: Capability,
    ) -> bool:
        """
        Determines whether this profile advertises the supplied
        capability.
        """
        return capability in self.capabilities

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.capabilities.display_text

    @property
    def display_description(self) -> str:
        return self.description

    def __str__(self) -> str:
        return self.display_name
