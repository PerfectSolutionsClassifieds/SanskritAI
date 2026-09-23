
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Lexical Adapter
--------------------------------

Stable adapter boundary for Monier-Williams lexical data.

Responsibilities
----------------

* source-specific lookup
* source-specific search
* structural normalization
* conversion from acquisition source records

The adapter does not construct canonical
DictionaryEntry / DictionarySense objects.

That responsibility belongs to ``MonierWilliamsMapper``.

Pipeline
--------

MonierWilliamsSourceRecord
        ↓
MonierWilliamsAdapter
        ↓
MonierWilliamsRecord
        ↓
MonierWilliamsMapper
        ↓
CanonicalDictionaryEntry / CanonicalDictionarySense

Version
-------
v0.7.0
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING

from .monier_williams_record import (
    MonierWilliamsRecord,
)

if TYPE_CHECKING:
    from SanskritAI.acquisition.lexical.monier_williams import (
        MonierWilliamsSourceRecord,
    )


class MonierWilliamsAdapter(ABC):
    """
    Abstract adapter contract for Monier-Williams data.
    """

    SOURCE = "monier-williams"

    # =========================================================
    # Metadata
    # =========================================================

    @property
    def source(self) -> str:
        """
        Return the canonical source identifier.
        """

        return self.SOURCE

    # =========================================================
    # Lookup
    # =========================================================

    @abstractmethod
    def lookup(
        self,
        headword: str,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Lookup a headword.
        """

        raise NotImplementedError

    # =========================================================
    # Search
    # =========================================================

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Search the external dictionary.
        """

        raise NotImplementedError

    # =========================================================
    # Enumeration
    # =========================================================

    @abstractmethod
    def all_records(
        self,
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Return all normalized records.
        """

        raise NotImplementedError

    # =========================================================
    # Cardinality
    # =========================================================

    @property
    def count(self) -> int:
        """
        Return the number of available records.
        """

        return len(
            self.all_records()
        )

    # =========================================================
    # Headword normalization
    # =========================================================

    @staticmethod
    def normalize_headword(
        value: str,
    ) -> str:
        """
        Conservatively normalize a headword for lookup.
        """

        if not isinstance(value, str):
            raise TypeError(
                "headword must be a string"
            )

        return " ".join(
            value.strip().split()
        )

    # =========================================================
    # Acquisition → Domain conversion
    # =========================================================

    @classmethod
    def from_source_record(
        cls,
        record: MonierWilliamsSourceRecord,
    ) -> MonierWilliamsRecord:
        """
        Convert an acquisition-stage
        ``MonierWilliamsSourceRecord`` into a normalized
        domain ``MonierWilliamsRecord``.

        This method performs structural normalization only.

        It does not:

        * perform linguistic analysis
        * create canonical entries
        * create canonical senses
        * perform repository registration
        * perform lookup
        """

        if record is None:
            raise TypeError(
                "record must be a MonierWilliamsSourceRecord"
            )

        fields = record.fields

        return MonierWilliamsRecord(
            headword=cls.normalize_headword(
                record.headword
            ),
            transliteration=(
                record.transliteration.strip()
                if isinstance(
                    record.transliteration,
                    str,
                )
                else ""
            ),
            definition=(
                record.definition.strip()
                if isinstance(
                    record.definition,
                    str,
                )
                else ""
            ),
            grammatical_label=(
                record.grammatical_label.strip()
                if isinstance(
                    record.grammatical_label,
                    str,
                )
                else ""
            ),
            grammatical_category=(
                record.grammatical_category.strip()
                if isinstance(
                    record.grammatical_category,
                    str,
                )
                else ""
            ),
            source=(
                record.source.strip()
                if isinstance(
                    record.source,
                    str,
                ) and record.source.strip()
                else cls.SOURCE
            ),
            source_id=(
                record.source_id.strip()
                if isinstance(
                    record.source_id,
                    str,
                )
                else ""
            ),
            source_reference=(
                record.source_reference.strip()
                if isinstance(
                    record.source_reference,
                    str,
                )
                else ""
            ),
            raw_text=(
                record.raw_text
                if isinstance(
                    record.raw_text,
                    str,
                )
                else ""
            ),
            homonym=(
                record.homonym.strip()
                if isinstance(
                    record.homonym,
                    str,
                )
                else ""
            ),
        )

    @classmethod
    def from_source_records(
        cls,
        records: Iterable[MonierWilliamsSourceRecord],
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Convert acquisition-stage source records into
        normalized domain records.
        """

        return tuple(
            cls.from_source_record(record)
            for record in records
        )

    # =========================================================
    # Record normalization
    # =========================================================

    @classmethod
    def normalize_record(
        cls,
        record: MonierWilliamsRecord,
    ) -> MonierWilliamsRecord:
        """
        Normalize textual fields without performing
        linguistic interpretation.

        All fields declared by MonierWilliamsRecord
        are preserved.
        """

        if not isinstance(
            record,
            MonierWilliamsRecord,
        ):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

        return MonierWilliamsRecord(
            headword=cls.normalize_headword(
                record.headword
            ),
            transliteration=(
                record.transliteration.strip()
                if isinstance(
                    record.transliteration,
                    str,
                )
                else ""
            ),
            definition=(
                record.definition.strip()
                if isinstance(
                    record.definition,
                    str,
                )
                else ""
            ),
            grammatical_label=(
                record.grammatical_label.strip()
                if isinstance(
                    record.grammatical_label,
                    str,
                )
                else ""
            ),
            grammatical_category=(
                record.grammatical_category.strip()
                if isinstance(
                    record.grammatical_category,
                    str,
                )
                else ""
            ),
            source=(
                record.source.strip()
                if isinstance(
                    record.source,
                    str,
                ) and record.source.strip()
                else cls.SOURCE
            ),
            source_id=(
                record.source_id.strip()
                if isinstance(
                    record.source_id,
                    str,
                )
                else ""
            ),
            source_reference=(
                record.source_reference.strip()
                if isinstance(
                    record.source_reference,
                    str,
                )
                else ""
            ),
            raw_text=(
                record.raw_text
                if isinstance(
                    record.raw_text,
                    str,
                )
                else ""
            ),
            homonym=(
                record.homonym.strip()
                if isinstance(
                    record.homonym,
                    str,
                )
                else ""
            ),
        )

    # =========================================================
    # Batch normalization
    # =========================================================

    @classmethod
    def normalize_records(
        cls,
        records: Iterable[MonierWilliamsRecord],
    ) -> tuple[MonierWilliamsRecord, ...]:
        """
        Normalize a sequence of domain records.
        """

        return tuple(
            cls.normalize_record(record)
            for record in records
        )
