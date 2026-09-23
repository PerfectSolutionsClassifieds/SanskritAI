
from __future__ import annotations

"""
SanskritAI
==========

Source Index

Purpose
-------
Indexes CanonicalDictionarySense objects by CanonicalSource.

Supported lookup dimensions:

    • source_id
    • canonical source name
    • abbreviated source name

The source-name and short-name indexes are many-to-one from
source metadata to dictionary senses.

Version
-------
3.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)


@dataclass(slots=True)
class SourceIndex:

    # ---------------------------------------------------------
    # Primary source-id index
    # ---------------------------------------------------------

    _index: dict[
        str,
        list[CanonicalDictionarySense],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Source name indexes
    # ---------------------------------------------------------

    _name_index: dict[
        str,
        list[CanonicalDictionarySense],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    _short_name_index: dict[
        str,
        list[CanonicalDictionarySense],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # =========================================================
    # Helpers
    # =========================================================

    @staticmethod
    def _normalise(
        value: Any,
    ) -> str:

        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def _append_unique(
        bucket: list[CanonicalDictionarySense],
        sense: CanonicalDictionarySense,
    ) -> None:

        if sense not in bucket:
            bucket.append(
                sense,
            )

    # =========================================================
    # Registration
    # =========================================================

    def add(
        self,
        source: CanonicalSource,
        sense: CanonicalDictionarySense,
    ) -> None:

        if source is None or sense is None:
            return

        source_id = self._normalise(
            source.source_id,
        )

        source_name = self._normalise(
            source.name,
        )

        short_name = self._normalise(
            source.short_name,
        )

        # -----------------------------------------------------
        # Source ID
        # -----------------------------------------------------

        if source_id:

            bucket = self._index.setdefault(
                source_id,
                [],
            )

            self._append_unique(
                bucket,
                sense,
            )

        # -----------------------------------------------------
        # Canonical source name
        # -----------------------------------------------------

        if source_name:

            bucket = self._name_index.setdefault(
                source_name,
                [],
            )

            self._append_unique(
                bucket,
                sense,
            )

        # -----------------------------------------------------
        # Short source name
        # -----------------------------------------------------

        if short_name:

            bucket = self._short_name_index.setdefault(
                short_name,
                [],
            )

            self._append_unique(
                bucket,
                sense,
            )

    # =========================================================
    # Source-ID Lookup
    # =========================================================

    def lookup(
        self,
        source_id: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:

        key = self._normalise(
            source_id,
        )

        return tuple(
            self._index.get(
                key,
                [],
            )
        )

    # =========================================================
    # Source Name Lookup
    # =========================================================

    def lookup_name(
        self,
        source_name: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:

        key = self._normalise(
            source_name,
        )

        return tuple(
            self._name_index.get(
                key,
                [],
            )
        )

    # =========================================================
    # Source Short Name Lookup
    # =========================================================

    def lookup_short_name(
        self,
        short_name: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:

        key = self._normalise(
            short_name,
        )

        return tuple(
            self._short_name_index.get(
                key,
                [],
            )
        )

    # =========================================================
    # Maintenance
    # =========================================================

    def clear(
        self,
    ) -> None:

        self._index.clear()
        self._name_index.clear()
        self._short_name_index.clear()

    # =========================================================
    # Diagnostics
    # =========================================================

    @property
    def source_count(
        self,
    ) -> int:

        return len(
            self._index,
        )

    @property
    def source_name_count(
        self,
    ) -> int:

        return len(
            self._name_index,
        )

    @property
    def source_short_name_count(
        self,
    ) -> int:

        return len(
            self._short_name_index,
        )

    def summary(
        self,
    ) -> dict:

        return {
            "sources": self.source_count,
            "source_names": self.source_name_count,
            "source_short_names": self.source_short_name_count,
        }

    # =========================================================
    # Python Protocol
    # =========================================================

    def __contains__(
        self,
        source_id: str,
    ) -> bool:

        return (
            self._normalise(
                source_id,
            )
            in self._index
        )

    def __len__(
        self,
    ) -> int:

        return self.source_count

    def __iter__(
        self,
    ):

        yield from sorted(
            self._index.keys(),
        )

    def __str__(
        self,
    ) -> str:

        return (
            "SourceIndex("
            f"{self.source_count} sources)"
        )
