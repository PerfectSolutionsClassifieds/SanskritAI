from __future__ import annotations

"""
SanskritAI
==========

Abstract Lexical Repository

Purpose
-------
Defines the canonical persistence contract for lexical
knowledge inside SanskritAI.

A repository stores canonical lexical records after
resource-specific transformation.

Pipeline
--------

Connector

    ↓

Parser

    ↓

Transformer

    ↓

CanonicalLexicalRecord

    ↓

AbstractLexicalRepository

Concrete implementations may persist data to

    • PostgreSQL
    • MongoDB
    • Redis
    • JSON
    • SQLite
    • REST API
    • In-memory collections

The repository is intentionally storage-agnostic.

Version
-------
1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable
from typing import Iterator

from SanskritAI.acquisition.knowledge.models.canonical_lexical_record import (
    CanonicalLexicalRecord,
)


@dataclass(slots=True)
class AbstractLexicalRepository(ABC):
    """
    Canonical lexical repository contract.
    """

    repository_name: str

    repository_version: str = "1.0.0"

    # ---------------------------------------------------------
    # Insert
    # ---------------------------------------------------------

    @abstractmethod
    def add(
        self,
        record: CanonicalLexicalRecord,
    ) -> None:
        """
        Inserts one canonical lexical record.
        """
        raise NotImplementedError

    def add_all(
        self,
        records: Iterable[
            CanonicalLexicalRecord,
        ],
    ) -> None:
        """
        Canonical batch insertion.
        """

        for record in records:

            self.add(
                record,
            )

    # ---------------------------------------------------------
    # Retrieval
    # ---------------------------------------------------------

    @abstractmethod
    def get(
        self,
        headword: str,
    ) -> tuple[
        CanonicalLexicalRecord,
        ...,
    ]:
        """
        Returns every canonical record matching the
        supplied headword.
        """
        raise NotImplementedError

    @abstractmethod
    def contains(
        self,
        headword: str,
    ) -> bool:
        """
        Returns True if the repository contains
        the supplied headword.
        """
        raise NotImplementedError

    @abstractmethod
    def all(
        self,
    ) -> tuple[
        CanonicalLexicalRecord,
        ...,
    ]:
        """
        Returns every canonical lexical record.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Maintenance
    # ---------------------------------------------------------

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """
        Removes every stored record.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def __iter__(
        self,
    ) -> Iterator[
        CanonicalLexicalRecord,
    ]:

        yield from self.all()

    def __len__(
        self,
    ) -> int:

        return self.count

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def count(
        self,
    ) -> int:
        """
        Number of stored lexical records.
        """
        raise NotImplementedError

    def summary(
        self,
    ) -> dict:

        return {

            "repository": self.repository_name,

            "version": self.repository_version,

            "records": self.count,

        }

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:

        return self.repository_name

    def __str__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(records={self.count})"
        )
