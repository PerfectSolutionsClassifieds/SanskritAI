from __future__ import annotations

"""
SanskritAI
==========

Service Resolver

Defines the canonical abstraction responsible for resolving
registered services from a ServiceCollection.

A ServiceResolver performs service lookup and selection based on
service keys. It is intentionally independent of lifetime
management and instance caching, which remain the responsibility
of ServiceContainer.

Architecture
------------

ServiceCollection
        │
        ▼
ServiceResolver
        │
        ▼
ServiceProvider

Version
-------
v0.7.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.dependency.service_collection import (
    ServiceCollection,
)
from SanskritAI.core.dependency.service_descriptor import (
    ServiceDescriptor,
)
from SanskritAI.core.dependency.service_key import ServiceKey
from SanskritAI.core.dependency.service_scope import (
    ServiceScope,
)


class ServiceResolver(ABC):
    """
    Abstract service resolution strategy.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def services(self) -> ServiceCollection:
        """
        Returns the available service collection.
        """
        raise NotImplementedError

    @abstractmethod
    def resolve(
        self,
        key: ServiceKey,
        *,
        scope: ServiceScope | None = None,
    ) -> ServiceDescriptor:
        """
        Resolves a service descriptor.

        Raises
        ------
        LookupError
            If the requested service cannot be resolved.
        """
        raise NotImplementedError

    def try_resolve(
        self,
        key: ServiceKey,
        *,
        scope: ServiceScope | None = None,
    ) -> ServiceDescriptor | None:
        """
        Attempts to resolve a service descriptor.

        Returns
        -------
        ServiceDescriptor | None
            The resolved descriptor, or None if no matching
            service exists.
        """
        try:
            return self.resolve(
                key,
                scope=scope,
            )
        except LookupError:
            return None

    def contains(
        self,
        key: ServiceKey,
    ) -> bool:
        """
        Determines whether a service exists.
        """
        return self.services.contains(key)
