from __future__ import annotations

"""
SanskritAI
==========

Capability Set

Defines the canonical immutable collection of capabilities
advertised by a component.

CapabilitySet is built around immutable set algebra rather than
lists, enabling efficient capability discovery, comparison,
negotiation, and composition.

Typical usages include:

- Parser capabilities
- Dictionary capabilities
- Corpus capabilities
- Plugin capabilities
- AI backend capabilities

Architecture
------------

ValueObject
      │
      ▼
CapabilitySet
      │
      └── frozenset[Capability]

Version
-------
v0.6.0
"""

from dataclasses import dataclass, field
from collections.abc import Iterator

from SanskritAI.core.capabilities.capability import Capability
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class CapabilitySet(ValueObject, Immutable, Displayable):
    """
    Immutable collection of capabilities.
    """

    capabilities: frozenset[Capability] = field(
        default_factory=frozenset
    )

    @property
    def count(self) -> int:
        """
        Returns the number of capabilities.
        """
        return len(self.capabilities)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no capabilities are present.
        """
        return self.count == 0

    def contains(
        self,
        capability: Capability,
    ) -> bool:
        """
        Determines whether the specified capability exists.
        """
        return capability in self.capabilities

    def add(
        self,
        capability: Capability,
    ) -> "CapabilitySet":
        """
        Returns a new CapabilitySet containing the supplied
        capability.
        """
        return CapabilitySet(
            self.capabilities | frozenset((capability,))
        )

    def remove(
        self,
        capability: Capability,
    ) -> "CapabilitySet":
        """
        Returns a new CapabilitySet without the supplied
        capability.
        """
        return CapabilitySet(
            self.capabilities - frozenset((capability,))
        )

    def union(
        self,
        other: "CapabilitySet",
    ) -> "CapabilitySet":
        """
        Returns the union of two capability sets.
        """
        return CapabilitySet(
            self.capabilities | other.capabilities
        )

    def intersection(
        self,
        other: "CapabilitySet",
    ) -> "CapabilitySet":
        """
        Returns the intersection of two capability sets.
        """
        return CapabilitySet(
            self.capabilities & other.capabilities
        )

    def difference(
        self,
        other: "CapabilitySet",
    ) -> "CapabilitySet":
        """
        Returns the set difference.
        """
        return CapabilitySet(
            self.capabilities - other.capabilities
        )

    def is_subset_of(
        self,
        other: "CapabilitySet",
    ) -> bool:
        """
        Determines whether this set is a subset of another.
        """
        return self.capabilities <= other.capabilities

    def is_superset_of(
        self,
        other: "CapabilitySet",
    ) -> bool:
        """
        Determines whether this set is a superset of another.
        """
        return self.capabilities >= other.capabilities

    @property
    def display_name(self) -> str:
        return f"{self.count} Capabilities"

    @property
    def display_text(self) -> str:
        return ", ".join(
            sorted(capability.display_name for capability in self.capabilities)
        )

    def __contains__(
        self,
        capability: Capability,
    ) -> bool:
        return capability in self.capabilities

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[Capability]:
        return iter(sorted(self.capabilities, key=lambda c: c.name))

    def __bool__(self) -> bool:
        return not self.is_empty

    def __str__(self) -> str:
        return self.display_text
