from __future__ import annotations

"""
SanskritAI
==========

Service Container

Defines the canonical runtime owner of the Dependency Injection
kernel.

A ServiceContainer owns the registered services together with the
resolver and provider used to access them.

The container intentionally remains immutable. Runtime caching of
singleton and scoped instances is considered an implementation
detail and may be introduced in future versions without changing
the public API.

Architecture
------------

ServiceCollection
        │
        ▼
ServiceResolver
        │
        ▼
ServiceProvider
        │
        ▼
ServiceContainer

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.dependency.service_collection import (
    ServiceCollection,
)
from SanskritAI.core.dependency.service_provider import (
    ServiceProvider,
)
from SanskritAI.core.dependency.service_resolver import (
    ServiceResolver,
)
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ServiceContainer(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable runtime dependency injection container.
    """

    services: ServiceCollection

    resolver: ServiceResolver

    provider: ServiceProvider

    @property
    def identifier(self) -> str:
        """
        Returns the canonical container identifier.
        """
        return self.__class__.__name__

    @property
    def service_count(self) -> int:
        """
        Returns the number of registered services.
        """
        return len(self.services)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no services are registered.
        """
        return self.services.is_empty

    @property
    def display_name(self) -> str:
        return "Service Container"

    @property
    def display_text(self) -> str:
        return (
            f"Service Container "
            f"({self.service_count} services)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Owns the Dependency Injection runtime "
            "configuration."
        )

    def __len__(self) -> int:
        return self.service_count

    def __bool__(self) -> bool:
        return not self.is_empty

    def __str__(self) -> str:
        return self.display_text
