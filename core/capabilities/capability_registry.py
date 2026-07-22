from __future__ import annotations

"""
SanskritAI
==========

Capability Registry

Defines the canonical immutable registry of capabilities.

Unlike the generic Registry kernel, this class is specialized
for managing Capability objects and provides capability-specific
operations while remaining immutable.

Architecture
------------

Registry
      │
      ▼
CapabilityRegistry
      │
      └── CapabilitySet

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from collections.abc import Iterator

from SanskritAI.core.capabilities.capability import Capability
from SanskritAI.core.capabilities.capability_set import CapabilitySet
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class CapabilityRegistry(ValueObject, Immutable, Displayable):
    """
    Immutable registry of capabilities.
    """

    capabilities: CapabilitySet = field(
        default_factory=CapabilitySet
    )

    @property
    def count(self) -> int:
        """
        Returns the number of registered capabilities.
        """
        return len(self.capabilities)

    def register(
        self,
        capability: Capability,
    ) -> "CapabilityRegistry":
        """
        Returns a new registry with the supplied capability
        registered.
        """
        return CapabilityRegistry(
            self.capabilities.add(capability)
        )

    def unregister(
        self,
        capability: Capability,
    ) -> "CapabilityRegistry":
        """
        Returns a new registry with the supplied capability
        removed.
        """
        return CapabilityRegistry(
            self.capabilities.remove(capability)
        )

    def contains(
        self,
        capability: Capability,
    ) -> bool:
        """
        Determines whether a capability is registered.
        """
        return capability in self.capabilities

    def lookup(
        self,
        name: str,
    ) -> Capability | None:
        """
        Looks up a capability by its canonical name.
        """
        normalized = name.strip().lower()

        for capability in self.capabilities:
            if capability.identifier == normalized:
                return capability

        return None

    @property
    def display_name(self) -> str:
        return f"{self.count} Registered Capabilities"

    @property
    def display_text(self) -> str:
        return self.capabilities.display_text

    def __contains__(
        self,
        capability: Capability,
    ) -> bool:
        return capability in self.capabilities

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[Capability]:
        return iter(self.capabilities)

    def __bool__(self) -> bool:
        return bool(self.capabilities)

    def __str__(self) -> str:
        return self.display_text
