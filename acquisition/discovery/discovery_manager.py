
from __future__ import annotations

"""
SanskritAI
==========

Discovery Manager

Coordinates corpus discovery across one or more discovery
providers.

Responsibilities
----------------
* Register discovery providers
* Execute enabled providers
* Aggregate discovery results
* Handle provider failures
* Optionally deduplicate discovered sources

The DiscoveryManager intentionally does NOT:

    • download resources
    • validate files
    • normalize content
    • import corpora

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from typing import Iterable

from SanskritAI.acquisition.discovery.base_discovery_provider import (
    BaseDiscoveryProvider,
)
from SanskritAI.acquisition.discovery.discovery_result import (
    DiscoveryResult,
)
from SanskritAI.acquisition.models.corpus_source import (
    CorpusSource,
)


class DiscoveryManager:
    """
    Coordinates discovery providers.
    """

    def __init__(
        self,
        *,
        deduplicate: bool = True,
    ) -> None:

        self._providers: list[BaseDiscoveryProvider] = []
        self._deduplicate = deduplicate

    # ---------------------------------------------------------
    # Provider Management
    # ---------------------------------------------------------

    def register(
        self,
        provider: BaseDiscoveryProvider,
    ) -> None:

        if not isinstance(provider, BaseDiscoveryProvider):
            raise TypeError(
                "provider must inherit from "
                "BaseDiscoveryProvider."
            )

        self._providers.append(provider)

    def unregister(
        self,
        provider: BaseDiscoveryProvider,
    ) -> None:

        self._providers.remove(provider)

    def clear(self) -> None:

        self._providers.clear()

    @property
    def providers(self) -> tuple[BaseDiscoveryProvider, ...]:
        return tuple(self._providers)

    @property
    def provider_count(self) -> int:
        return len(self._providers)

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(self) -> DiscoveryResult:

        result = DiscoveryResult()

        seen: set[str] = set()

        for provider in self._providers:

            if not provider.enabled:
                continue

            try:

                provider.initialize()

                sources = provider.discover()

                result.add_provider(
                    provider.name,
                    success=True,
                )

                for source in sources:

                    key = self._deduplication_key(source)

                    if (
                        self._deduplicate
                        and key in seen
                    ):
                        result.statistics.duplicate_sources += 1
                        continue

                    seen.add(key)

                    result.add_source(source)

                provider.shutdown()

            except Exception as exc:

                result.add_provider(
                    provider.name,
                    success=False,
                )

                result.add_error(
                    f"{provider.name}: {exc}"
                )

                try:
                    provider.shutdown()
                except Exception:
                    pass

        result.complete()

        return result

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def discover_provider(
        self,
        provider: BaseDiscoveryProvider,
    ) -> DiscoveryResult:
        """
        Executes a single provider.
        """

        manager = DiscoveryManager(
            deduplicate=self._deduplicate,
        )

        manager.register(provider)

        return manager.discover()

    @staticmethod
    def _deduplication_key(
        source: CorpusSource,
    ) -> str:
        """
        Returns a stable key used for deduplication.

        Preference order:

            identifier
            download URL
            local path
            title
        """

        for attr in (
            "identifier",
            "download_url",
            "local_path",
            "title",
        ):
            value = getattr(
                source,
                attr,
                None,
            )

            if value:
                return str(value).lower()

        return repr(source).lower()

    # ---------------------------------------------------------
    # Container Protocol
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return len(self._providers)

    def __iter__(self):
        return iter(self._providers)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "DiscoveryManager("
            f"providers={len(self)}, "
            f"deduplicate={self._deduplicate})"
        )
