from __future__ import annotations

"""
SanskritAI
==========

Monier-Williams Lexical Adapter
--------------------------------

Adapter boundary for integrating the Monier-Williams Sanskrit-English
dictionary with the SanskritAI lexical domain.

Architecture
------------

External MW Source
        |
        v
MonierWilliamsAdapter
        |
        v
MonierWilliamsRecord
        |
        v
Canonical Lexical Model
        |
        v
CanonicalKnowledgeRepository

Design Principles
-----------------

1. External dictionary representation remains outside the domain model.
2. The adapter does not perform linguistic reasoning.
3. The adapter does not replace the canonical repository.
4. Lookup is source-specific.
5. Normalization is deterministic.
6. Actual MW data loading can be introduced independently.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Optional

from .monier_williams_record import MonierWilliamsRecord


class MonierWilliamsAdapter(ABC):
    """
    Abstract adapter contract for Monier-Williams data.

    Concrete implementations may later read:

        * XML
        * JSON
        * CSV
        * SQLite
        * locally indexed source data

    The lexical domain should depend on this stable contract rather
    than on the external source format.
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

        Parameters
        ----------
        headword:
            Sanskrit dictionary headword.

        Returns
        -------
        tuple[MonierWilliamsRecord, ...]
            Zero or more matching records.
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

        Concrete implementations determine whether the search is:

            * exact
            * prefix
            * normalized
            * indexed
            * full-text

        The adapter contract deliberately does not prescribe
        the implementation.
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

        The default implementation derives the value from
        all_records(). Concrete indexed implementations may
        override this for efficiency.
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
        Normalize a headword for adapter-level lookup.

        This is intentionally conservative.

        No Sanskrit linguistic transformation is performed here.
        """
        if not isinstance(value, str):
            raise TypeError("headword must be a string")

        return " ".join(value.strip().split())

    # =========================================================
    # Record normalization
    # =========================================================

    @classmethod
    def normalize_record(
        cls,
        record: MonierWilliamsRecord,
    ) -> MonierWilliamsRecord:
        """
        Normalize a Monier-Williams record.

        The method performs only structural text normalization.
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
            source=(
                record.source.strip()
                if isinstance(record.source, str)
                else cls.SOURCE
            ),
            source_id=(
                record.source_id.strip()
                if isinstance(record.source_id, str)
                else ""
            ),
            raw_text=(
                record.raw_text
                if isinstance(record.raw_text, str)
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
