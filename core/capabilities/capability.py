from __future__ import annotations

"""
SanskritAI
==========

Capability

Defines the canonical immutable capability advertised by a
component within the SanskritAI ecosystem.

A Capability represents a semantic feature that a component
provides at runtime. Unlike Contracts, which describe required
behavior, Capabilities describe optional or discoverable
features.

Typical examples include:

- morphology
- sandhi
- samasa
- tokenization
- search
- serialization
- ai_embeddings
- vector_search

Architecture
------------

ValueObject
      │
      ▼
Capability
      │
      ▼
CapabilitySet

Version
-------
v0.6.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Capability(ValueObject, Immutable, Displayable):
    """
    Immutable semantic capability.
    """

    name: str

    description: str = ""

    def __post_init__(self) -> None:
        normalized = self.name.strip().lower()

        if not normalized:
            raise ValueError(
                "Capability name cannot be empty."
            )

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """
        Canonical identifier.
        """
        return self.name

    @property
    def display_name(self) -> str:
        """
        Human-readable capability name.
        """
        return self.name.replace("_", " ").title()

    @property
    def display_description(self) -> str:
        """
        Optional capability description.
        """
        return self.description

    def matches(
        self,
        name: str,
    ) -> bool:
        """
        Determines whether the supplied name refers to this
        capability.
        """
        return self.name == name.strip().lower()

    def __str__(self) -> str:
        return self.name
