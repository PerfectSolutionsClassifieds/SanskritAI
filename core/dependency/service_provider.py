from __future__ import annotations

"""
SanskritAI
==========

Service Provider

Defines the public façade for dependency resolution.

A ServiceProvider delegates descriptor resolution to a
ServiceResolver and service creation to the associated
ServiceFactory through the resolved ServiceDescriptor.

The provider intentionally performs no lifetime management.
Singleton, scoped, and transient semantics are implemented by
ServiceContainer.

Architecture
------------

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
from typing import Any

from SanskritAI.core.dependency.service_key import ServiceKey
from SanskritAI.core.dependency.service_resolver import (
    ServiceResolver,
)
from SanskritAI.core.dependency.service_scope import (
    ServiceScope,
)
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ServiceProvider(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Public façade for dependency resolution.
    """

    resolver: ServiceResolver

    @property
    def identifier(self) -> str:
        """
        Returns the provider identifier.
        """
        return self.__class__.__name__

    def contains(
        self,
        key: ServiceKey,
    ) -> bool:
        """
        Determines whether the supplied service exists.
        """
        return self.resolver.contains(key)

    def get_descriptor(
        self,
        key: ServiceKey,
        *,
        scope: ServiceScope | None = None,
    ):
        """
        Resolves a service descriptor.
        """
        return self.resolver.resolve(
            key,
            scope=scope,
        )

    def get_service(
        self,
        key: ServiceKey,
        *,
        scope: ServiceScope | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Creates a new service instance.

        Lifetime management is intentionally delegated to
        ServiceContainer.
        """
        descriptor = self.get_descriptor(
            key,
            scope=scope,
        )

        return descriptor.create(**kwargs)

    @property
    def display_name(self) -> str:
        return "Service Provider"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Public façade for dependency resolution."
        )

    def __str__(self) -> str:
        return self.display_name
