from __future__ import annotations

"""
SanskritAI
==========

Service Descriptor

Defines the canonical immutable description of a service
registered within the Dependency Injection kernel.

A ServiceDescriptor combines the semantic identity, lifetime,
and factory responsible for creating a service instance.

It intentionally contains no mutable state and performs no
service resolution. Resolution is the responsibility of
ServiceProvider and ServiceContainer.

Architecture
------------

ValueObject
      │
      ▼
ServiceDescriptor
      │
      ├── ServiceKey
      ├── ServiceLifetime
      ├── ServiceFactory
      └── description

Version
-------
v0.7.0
"""

from dataclasses import dataclass

from SanskritAI.core.dependency.service_factory import ServiceFactory
from SanskritAI.core.dependency.service_key import ServiceKey
from SanskritAI.core.dependency.service_lifetime import ServiceLifetime
from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ServiceDescriptor(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable description of a registered service.
    """

    key: ServiceKey

    lifetime: ServiceLifetime

    factory: ServiceFactory

    description: str = ""

    @property
    def identifier(self) -> str:
        """
        Returns the fully-qualified service identifier.
        """
        return self.key.identifier

    @property
    def service_type(self):
        """
        Returns the semantic service type.
        """
        return self.key.service_type

    @property
    def display_name(self) -> str:
        """
        Returns the human-readable service name.
        """
        return self.key.display_name

    @property
    def display_text(self) -> str:
        """
        Returns the canonical display representation.
        """
        return (
            f"{self.key.display_text}"
            f" [{self.lifetime.display_name}]"
        )

    @property
    def display_description(self) -> str:
        """
        Returns the optional service description.
        """
        if self.description:
            return self.description

        return (
            f"{self.service_type.display_name} "
            f"service using "
            f"{self.lifetime.display_name.lower()} "
            f"lifetime."
        )

    @property
    def is_singleton(self) -> bool:
        return self.lifetime.is_singleton

    @property
    def is_scoped(self) -> bool:
        return self.lifetime.is_scoped

    @property
    def is_transient(self) -> bool:
        return self.lifetime.is_transient

    def create(
        self,
        *args,
        **kwargs,
    ):
        """
        Creates a service instance through the associated
        ServiceFactory.
        """
        return self.factory(*args, **kwargs)

    def __str__(self) -> str:
        return self.display_text
