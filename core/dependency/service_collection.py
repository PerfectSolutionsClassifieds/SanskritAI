from __future__ import annotations

"""
SanskritAI
==========

Service Collection

Defines the canonical immutable collection of service
descriptors.

A ServiceCollection serves as the central repository of service
descriptions prior to runtime resolution. It provides immutable
registration, lookup, iteration, and replacement semantics.

Architecture
------------

ValueObject
      │
      ▼
ServiceCollection
      │
      └── frozenset[ServiceDescriptor]

Version
-------
v0.7.0
"""

from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field

from SanskritAI.core.dependency.service_descriptor import (
    ServiceDescriptor,
)
from SanskritAI.core.dependency.service_key import ServiceKey
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ServiceCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of service descriptors.
    """

    services: frozenset[ServiceDescriptor] = field(
        default_factory=frozenset
    )

    @property
    def count(self) -> int:
        """
        Returns the number of registered services.
        """
        return len(self.services)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if the collection contains no services.
        """
        return self.count == 0

    def contains(
        self,
        key: ServiceKey,
    ) -> bool:
        """
        Determines whether the supplied service key exists.
        """
        return self.lookup(key) is not None

    def lookup(
        self,
        key: ServiceKey,
    ) -> ServiceDescriptor | None:
        """
        Looks up a service descriptor by key.
        """
        for descriptor in self.services:
            if descriptor.key == key:
                return descriptor

        return None

    def add(
        self,
        descriptor: ServiceDescriptor,
    ) -> "ServiceCollection":
        """
        Returns a new collection containing the supplied
        descriptor.

        Existing descriptors with the same key are replaced.
        """
        remaining = frozenset(
            service
            for service in self.services
            if service.key != descriptor.key
        )

        return ServiceCollection(
            remaining | frozenset((descriptor,))
        )

    def remove(
        self,
        key: ServiceKey,
    ) -> "ServiceCollection":
        """
        Returns a new collection without the supplied key.
        """
        return ServiceCollection(
            frozenset(
                service
                for service in self.services
                if service.key != key
            )
        )

    @property
    def display_name(self) -> str:
        return f"{self.count} Services"

    @property
    def display_text(self) -> str:
        return ", ".join(
            sorted(
                service.identifier
                for service in self.services
            )
        )

    def __contains__(
        self,
        key: ServiceKey,
    ) -> bool:
        return self.contains(key)

    def __len__(self) -> int:
        return self.count

    def __iter__(self) -> Iterator[ServiceDescriptor]:
        return iter(
            sorted(
                self.services,
                key=lambda service: service.identifier,
            )
        )

    def __bool__(self) -> bool:
        return not self.is_empty

    def __str__(self) -> str:
        return self.display_text
