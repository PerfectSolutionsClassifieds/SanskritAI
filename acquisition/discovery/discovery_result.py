
from __future__ import annotations

"""
SanskritAI
==========

Discovery Result

Standardized result object returned by every corpus discovery
operation.

The DiscoveryResult aggregates all information produced during a
discovery session, including:

    • discovered corpus sources
    • participating providers
    • discovery statistics
    • warnings
    • errors
    • elapsed execution time

This mirrors the architecture of:

    • AcquisitionResult
    • ImportResult

ensuring a consistent result model throughout the acquisition
pipeline.

Version
-------
v0.5.0

Author
------
SanskritAI Project
"""

from dataclasses import dataclass, field
from datetime import datetime
from time import perf_counter
from typing import Iterable

from SanskritAI.acquisition.models.corpus_source import CorpusSource


@dataclass(slots=True)
class DiscoveryStatistics:
    """
    Statistics collected during corpus discovery.
    """

    providers_visited: int = 0
    providers_succeeded: int = 0
    providers_failed: int = 0

    sources_discovered: int = 0
    duplicate_sources: int = 0
    skipped_sources: int = 0

    elapsed_seconds: float = 0.0

    @property
    def total_providers(self) -> int:
        return self.providers_visited

    @property
    def total_sources(self) -> int:
        return self.sources_discovered


@dataclass(slots=True)
class DiscoveryResult:
    """
    Result returned by a corpus discovery operation.
    """

    discovered_sources: list[CorpusSource] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    providers: list[str] = field(
        default_factory=list
    )

    statistics: DiscoveryStatistics = field(
        default_factory=DiscoveryStatistics
    )

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    finished_at: datetime | None = None

    # Internal timer

    _start_time: float = field(
        default_factory=perf_counter,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def complete(self) -> None:
        """
        Marks discovery as completed.
        """

        self.finished_at = datetime.utcnow()

        self.statistics.elapsed_seconds = (
            perf_counter() - self._start_time
        )

    # ---------------------------------------------------------
    # Source Management
    # ---------------------------------------------------------

    def add_source(
        self,
        source: CorpusSource,
    ) -> None:
        """
        Adds a discovered corpus source.
        """

        self.discovered_sources.append(source)

        self.statistics.sources_discovered += 1

    def extend_sources(
        self,
        sources: Iterable[CorpusSource],
    ) -> None:
        """
        Adds multiple discovered sources.
        """

        for source in sources:
            self.add_source(source)

    # ---------------------------------------------------------
    # Provider Management
    # ---------------------------------------------------------

    def add_provider(
        self,
        provider_name: str,
        *,
        success: bool = True,
    ) -> None:
        """
        Records execution of a provider.
        """

        self.providers.append(provider_name)

        self.statistics.providers_visited += 1

        if success:
            self.statistics.providers_succeeded += 1
        else:
            self.statistics.providers_failed += 1

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def add_warning(
        self,
        message: str,
    ) -> None:
        self.warnings.append(message)

    def add_error(
        self,
        message: str,
    ) -> None:
        self.errors.append(message)

    @property
    def success(self) -> bool:
        """
        Returns True when discovery completed without errors.
        """
        return len(self.errors) == 0

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def source_count(self) -> int:
        return len(self.discovered_sources)

    @property
    def provider_count(self) -> int:
        return len(self.providers)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.source_count

    def __bool__(self) -> bool:
        return self.success

    def __repr__(self) -> str:

        return (
            "DiscoveryResult("
            f"sources={self.source_count}, "
            f"providers={self.provider_count}, "
            f"warnings={len(self.warnings)}, "
            f"errors={len(self.errors)}, "
            f"elapsed={self.statistics.elapsed_seconds:.3f}s)"
        )
