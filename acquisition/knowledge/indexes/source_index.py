
from __future__ import annotations

"""
SanskritAI
==========

Source Index

Purpose
-------
Indexes CanonicalDictionarySense objects by CanonicalSource.source_id.

The index accepts both:

    • a source identifier string
    • a CanonicalSource object

This keeps the index convenient for both low-level lookup and
canonical object-graph traversal.

Version
-------
2.1.0
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

    _index: dict[
        str,
        list[CanonicalDictionarySense],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # =========================================================
    # Registration
    # =========================================================

    def add(
        self,
        source: CanonicalSource,
        sense: CanonicalDictionarySense,
    ) -> None:
        """
        Add one dictionary sense under its canonical source id.
        """

        source_id = self._normalize_source_id(
            source,
        )

        if not source_id:
            return

        bucket = self._index.setdefault(
            source_id,
            [],
        )

        bucket.append(
            sense,
        )

    # =========================================================
    # Lookup
    # =========================================================

    def lookup(
        self,
        source: str | CanonicalSource,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:
        """
        Lookup dictionary senses by source.

        Parameters
        ----------
        source:
            Either a source identifier string or a CanonicalSource
            instance.

        Returns
        -------
        tuple[CanonicalDictionarySense, ...]
            All senses indexed under the source identifier.
        """

        source_id = self._normalize_source_id(
            source,
        )

        if not source_id:
            return ()

        return tuple(
            self._index.get(
                source_id,
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
        """
        Lookup senses by canonical source name.
        """

        normalized = source_name.strip()

        if not normalized:
            return ()

        matches: list[
            CanonicalDictionarySense
        ] = []

        for sense_list in self._index.values():

            for sense in sense_list:

                source = getattr(
                    sense,
                    "source",
                    None,
                )

                if source is None:
                    continue

                if getattr(
                    source,
                    "name",
                    None,
                ) == normalized:

                    matches.append(
                        sense,
                    )

        return tuple(
            matches,
        )

    # =========================================================
    # Short Name Lookup
    # =========================================================

    def lookup_short_name(
        self,
        short_name: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:
        """
        Lookup senses by abbreviated source name.
        """

        normalized = short_name.strip()

        if not normalized:
            return ()

        matches: list[
            CanonicalDictionarySense
        ] = []

        for sense_list in self._index.values():

            for sense in sense_list:

                source = getattr(
                    sense,
                    "source",
                    None,
                )

                if source is None:
                    continue

                if getattr(
                    source,
                    "short_name",
                    None,
                ) == normalized:

                    matches.append(
                        sense,
                    )

        return tuple(
            matches,
        )

    # =========================================================
    # Normalization
    # =========================================================

    @staticmethod
    def _normalize_source_id(
        source: str | CanonicalSource | Any,
    ) -> str:
        """
        Convert a source identifier or CanonicalSource object
        into the canonical source-id string.
        """

        if isinstance(
            source,
            CanonicalSource,
        ):
            return source.source_id.strip()

        if isinstance(
            source,
            str,
        ):
            return source.strip()

        source_id = getattr(
            source,
            "source_id",
            None,
        )

        if isinstance(
            source_id,
            str,
        ):
            return source_id.strip()

        return ""

    # =========================================================
    # Maintenance
    # =========================================================

    def clear(
        self,
    ) -> None:
        """
        Remove all indexed source information.
        """

        self._index.clear()

    # =========================================================
    # Diagnostics
    # =========================================================

    @property
    def source_count(
        self,
    ) -> int:
        """
        Number of unique indexed sources.
        """

        return len(
            self._index,
        )

    def summary(
        self,
    ) -> dict:
        """
        Return index diagnostics.
        """

        return {
            "sources": self.source_count,
        }

    # =========================================================
    # Python Protocol
    # =========================================================

    def __contains__(
        self,
        source: str | CanonicalSource,
    ) -> bool:

        source_id = self._normalize_source_id(
            source,
        )

        return (
            bool(source_id)
            and source_id in self._index
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
