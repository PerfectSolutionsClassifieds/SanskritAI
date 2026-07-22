
from __future__ import annotations

"""
SanskritAI
==========

Discovery Registry

Maintains the collection of registered corpus discovery providers.

Responsibilities
----------------
* Register providers
* Remove providers
* Lookup providers
* Enumerate providers
* Prevent duplicate registration

The registry intentionally does NOT:

    • execute discovery
    • download resources
    • validate resources
    • normalize text
    • import corpora

Those responsibilities belong to DiscoveryManager.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from collections.abc import Iterator

from SanskritAI.acquisition.discovery.base_discovery_provider import (
    BaseDiscoveryProvider,
)


class DiscoveryRegistry:
    """
    Registry of discovery providers.
    """

    def __init__(self) -> None:

        self._providers: dict[
            str,
            BaseDiscoveryProvider,
        ] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        provider: BaseDiscoveryProvider,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Registers a discovery provider.
        """

        if not isinstance(
            provider,
            BaseDiscoveryProvider,
        ):
            raise TypeError(
                "provider must inherit from "
                "BaseDiscoveryProvider."
            )

        name = provider.name

        if (
            name in self._providers
            and not overwrite
        ):
            raise ValueError(
                f"Provider '{name}' is already registered."
            )

        self._providers[name] = provider

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Removes a provider.
        """

        self._providers.pop(name)

    def clear(self) -> None:
        """
        Removes every provider.
        """

        self._providers.clear()

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        name: str,
    ) -> BaseDiscoveryProvider | None:
        """
        Returns a provider by name.
        """

        return self._providers.get(name)

    def require(
        self,
        name: str,
    ) -> BaseDiscoveryProvider:
        """
        Returns a provider or raises KeyError.
        """

        provider = self.get(name)

        if provider is None:
            raise KeyError(
                f"No provider named '{name}'."
            )

        return provider

    def contains(
        self,
        name: str,
    ) -> bool:
        """
        Returns True if a provider exists.
        """

        return name in self._providers

    # ------------------------------------------------------------------
    # Enumeration
    # ------------------------------------------------------------------

    @property
    def providers(
        self,
    ) -> tuple[BaseDiscoveryProvider, ...]:
        """
        Returns every registered provider.
        """

        return tuple(
            self._providers.values()
        )

    @property
    def enabled_providers(
        self,
    ) -> tuple[BaseDiscoveryProvider, ...]:
        """
        Returns enabled providers only.
        """

        return tuple(
            provider
            for provider in self._providers.values()
            if provider.enabled
        )

    @property
    def disabled_providers(
        self,
    ) -> tuple[BaseDiscoveryProvider, ...]:
        """
        Returns disabled providers.
        """

        return tuple(
            provider
            for provider in self._providers.values()
            if not provider.enabled
        )

    @property
    def provider_names(
        self,
    ) -> tuple[str, ...]:
        """
        Returns registered provider names.
        """

        return tuple(
            self._providers.keys()
        )

    @property
    def count(self) -> int:
        """
        Number of registered providers.
        """

        return len(self._providers)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no providers are registered.
        """

        return not self._providers

    # ------------------------------------------------------------------
    # Bulk Operations
    # ------------------------------------------------------------------

    def register_many(
        self,
        providers,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Registers multiple providers.
        """

        for provider in providers:
            self.register(
                provider,
                overwrite=overwrite,
            )

    def enable_all(self) -> None:
        """
        Enables every provider.
        """

        for provider in self._providers.values():
            provider.enabled = True

    def disable_all(self) -> None:
        """
        Disables every provider.
        """

        for provider in self._providers.values():
            provider.enabled = False

    # ------------------------------------------------------------------
    # Container Protocol
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return self.count

    def __iter__(
        self,
    ) -> Iterator[BaseDiscoveryProvider]:
        return iter(
            self._providers.values()
        )

    def __contains__(
        self,
        name: str,
    ) -> bool:
        return self.contains(name)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "DiscoveryRegistry("
            f"providers={self.count})"
        )
