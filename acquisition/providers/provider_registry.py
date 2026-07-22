
from __future__ import annotations

"""
SanskritAI
==========

Provider Registry

Central registry for all Acquisition Providers.

The ProviderRegistry maintains the collection of all registered
providers capable of acquiring corpus resources from external
repositories.

Responsibilities
----------------
* Register providers
* Lookup providers
* Remove providers
* Enumerate providers
* Provider metadata
* Health reporting

Architecture
------------

                ProviderRegistry
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
 GretilProvider   GitHubProvider   SaritProvider
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                 AcquisitionManager

The registry intentionally knows nothing about repositories,
downloaders, or importers. It simply manages provider instances.

Version
-------
v0.7.0
"""

from typing import Iterator

from SanskritAI.acquisition.providers.base_provider import (
    BaseProvider,
)
from SanskritAI.core.registry.base_registry import (
    BaseRegistry,
)


class ProviderRegistry(BaseRegistry[BaseProvider]):
    """
    Registry of acquisition providers.
    """

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        provider: BaseProvider,
        *,
        replace: bool = False,
    ) -> None:
        """
        Register a provider.
        """

        identifier = provider.identifier.lower()

        if (
            identifier in self._entries
            and not replace
        ):
            raise ValueError(
                f"Provider '{identifier}' "
                "is already registered."
            )

        self._entries[identifier] = provider

    # ---------------------------------------------------------

    def unregister(
        self,
        identifier: str,
    ) -> bool:
        """
        Remove a provider.
        """

        identifier = identifier.lower()

        if identifier not in self._entries:
            return False

        del self._entries[identifier]

        return True

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def provider(
        self,
        identifier: str,
    ) -> BaseProvider:
        """
        Retrieve a provider.
        """

        identifier = identifier.lower()

        if identifier not in self._entries:
            raise KeyError(
                f"Unknown provider '{identifier}'."
            )

        return self._entries[identifier]

    # ---------------------------------------------------------

    def exists(
        self,
        identifier: str,
    ) -> bool:
        """
        Determine whether a provider exists.
        """

        return (
            identifier.lower()
            in self._entries
        )

    # ---------------------------------------------------------
    # Reporting
    # ---------------------------------------------------------

    def identifiers(
        self,
    ) -> tuple[str, ...]:
        """
        Registered provider identifiers.
        """

        return tuple(
            sorted(self._entries.keys())
        )

    # ---------------------------------------------------------

    def providers(
        self,
    ) -> tuple[BaseProvider, ...]:
        """
        Registered provider instances.
        """

        return tuple(
            self._entries.values()
        )

    # ---------------------------------------------------------

    def metadata(
        self,
    ) -> dict:
        """
        Registry metadata.
        """

        return {
            "provider_count": len(self),
            "providers": list(
                self.identifiers()
            ),
        }

    # ---------------------------------------------------------

    def health_report(
        self,
    ) -> dict[str, bool]:
        """
        Report provider availability.

        Future providers may override
        BaseProvider.health_check() for
        network/service diagnostics.
        """

        report: dict[str, bool] = {}

        for identifier, provider in self._entries.items():

            try:

                if hasattr(
                    provider,
                    "health_check",
                ):
                    report[identifier] = bool(
                        provider.health_check()
                    )
                else:
                    report[identifier] = True

            except Exception:
                report[identifier] = False

        return report

    # ---------------------------------------------------------
    # Collection Protocol
    # ---------------------------------------------------------

    def __contains__(
        self,
        identifier: str,
    ) -> bool:

        return self.exists(identifier)

    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[BaseProvider]:

        return iter(
            self._entries.values()
        )

    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._entries
        )

    # ---------------------------------------------------------

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"providers={len(self)})"
        )
