
from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Lexical Adapter
--------------------------------

Stable adapter boundary for Monier-Williams lexical data.

The adapter is responsible for:

* source-specific lookup
* source-specific search
* structural normalization

It does not construct canonical DictionaryEntry or DictionarySense
objects. That responsibility belongs to MonierWilliamsMapper.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable

from .monier_williams_record import (
    MonierWilliamsRecord,
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

        return len(self.all_records())

    # =========================================================
    # Normalization
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
    # Record normalization
    # =========================================================

    @classmethod
    def normalize_record(
        cls,
        record: MonierWilliamsRecord,
    ) -> MonierWilliamsRecord:
        """
        Normalize textual fields without performing linguistic
        interpretation.

        All fields declared by MonierWilliamsRecord are preserved.
        """

        if not isinstance(record, MonierWilliamsRecord):
            raise TypeError(
                "record must be a MonierWilliamsRecord"
            )

        return MonierWilliamsRecord(
            headword=cls.normalize_headword(
                record.headword,
            ),
            transliteration=(
                record.transliteration.strip()
                if isinstance(record.transliteration, str)
                else ""
            ),
            definition=(
                record.definition.strip()
                if isinstance(record.definition, str)
                else ""
            ),
            grammatical_label=(
                record.grammatical_label.strip()
                if isinstance(record.grammatical_label, str)
                else ""
            ),
            grammatical_category=(
                record.grammatical_category.strip()
                if isinstance(record.grammatical_category, str)
                else ""
            ),
            source=(
                record.source.strip()
                if isinstance(record.source, str)
                and record.source.strip()
                else cls.SOURCE
            ),
            source_id=(
                record.source_id.strip()
                if isinstance(record.source_id, str)
                else ""
            ),
            source_reference=(
                record.source_reference.strip()
                if isinstance(record.source_reference, str)
                else ""
            ),
            raw_text=(
                record.raw_text
                if isinstance(record.raw_text, str)
                else ""
            ),
            homonym=(
                record.homonym.strip()
                if isinstance(record.homonym, str)
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
        Normalize a sequence of records.
        """

        return tuple(
            cls.normalize_record(record)
            for record in records
        )
