
from __future__ import annotations

"""
SanskritAI
==========

In-Memory Monier-Williams Adapter
---------------------------------

Small deterministic implementation used for:

* unit tests
* development
* integration testing
* adapter contract verification

It is not intended to be the final MW storage implementation.

Version
-------
v0.7.0
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable

from .monier_williams_adapter import (
    MonierWilliamsAdapter,
)
from .monier_williams_record import (
    MonierWilliamsRecord,
)

if TYPE_CHECKING:
    from SanskritAI.acquisition.lexical.monier_williams import (
        MonierWilliamsSourceRecord,
    )


@dataclass(slots=True)
class InMemoryMonierWilliamsAdapter(
    MonierWilliamsAdapter,
):
    """
    In-memory implementation of the
    Monier-Williams adapter.
    """

    records: tuple[MonierWilliamsRecord, ...] = ()

    def __init__(
        self,
        records: Iterable[MonierWilliamsRecord] = (),
    ) -> None:
        self.records = self.normalize_records(
            records
        )

    # =========================================================
    # Acquisition construction
    # =========================================================

    @classmethod
    def from_source_records(
        cls,
        records: Iterable[MonierWilliamsSourceRecord],
    ) -> InMemoryMonierWilliamsAdapter:
        """
        Construct an in-memory adapter from
        acquisition-stage MW source records.
        """

        return cls(
            cls.from_source_records_to_domain(
                records
            )
        )

    @classmethod
    def from_source_records_to_domain(
        cls,
        records: Iterable[MonierWilliamsSourceRecord],
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Convert acquisition records into normalized
        domain records.

        Kept as a small explicit bridge for deterministic
        integration testing.
        """

        return cls.__mro__[1].from_source_records(
            records
        )

    # =========================================================
    # Lookup
    # =========================================================

    def lookup(
        self,
        headword: str,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Lookup exact normalized headword.
        """

        normalized = self.normalize_headword(
            headword
        )

        return tuple(
            record
            for record in self.records
            if record.headword == normalized
        )

    # =========================================================
    # Search
    # =========================================================

    def search(
        self,
        query: str,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Search headword, definition,
        and transliteration.
        """

        normalized = (
            self.normalize_headword(query)
            .casefold()
        )

        if not normalized:
            return ()

        return tuple(
            record
            for record in self.records
            if (
                normalized
                in record.headword.casefold()
                or normalized
                in record.definition.casefold()
                or normalized
                in record.transliteration.casefold()
            )
        )

    # =========================================================
    # Enumeration
    # =========================================================

    def all_records(
        self,
    ) -> tuple[MonierWilliamsRecord, ...]:
        return self.records

    # =========================================================
    # Count
    # =========================================================

    @property
    def count(self) -> int:
        return len(self.records)
