from __future__ import annotations

"""
SanskritAI
==========

Canonical Lexical Repository

Purpose
-------
The CanonicalLexicalRepository is the first persistent
knowledge layer of the Canonical Sanskrit Knowledge Repository.

It is intentionally independent of

    • Monier–Williams

    • Apte

    • Amarakośa

    • Śabdakalpadruma

    • Vācaspatyam

    • Dhātupāṭha

    • Gaṇapāṭha

    • Uṇādi

Every lexical resource ultimately contributes
CanonicalLexicalRecord objects into this repository.

Architecture
------------

External Resource

        ↓

Parser

        ↓

RawLexicalEntry

        ↓

Transformer

        ↓

CanonicalLexicalRecord

        ↓

CanonicalLexicalRepository

        ↓

Exporters

            JSON

            PostgreSQL

            MongoDB

            Redis

            REST API

Design Principles
-----------------

• Canonical

• Immutable inserts

• Source independent

• Fast lookup

• No parser logic

• No storage-engine logic

• No grammatical inference

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Iterable

from SanskritAI.acquisition.knowledge.transformers.monier_williams_transformer import (
    CanonicalLexicalRecord,
)


@dataclass(slots=True)
class CanonicalLexicalRepository:
    """
    In-memory canonical lexical repository.

    This repository becomes the single source of truth
    before export into any persistence backend.
    """

    _records: dict[
        str,
        list[CanonicalLexicalRecord],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Insert
    # ---------------------------------------------------------

    def add(
        self,
        record: CanonicalLexicalRecord,
    ) -> None:
        """
        Adds one canonical lexical record.

        Multiple dictionary sources may share the
        same headword.
        """

        key = record.headword

        self._records.setdefault(
            key,
            [],
        ).append(
            record,
        )

    def add_all(
        self,
        records: Iterable[
            CanonicalLexicalRecord,
        ],
    ) -> None:
        """
        Adds multiple records.
        """

        for record in records:

            self.add(
                record,
            )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def contains(
        self,
        headword: str,
    ) -> bool:
        """
        Returns True if a headword exists.
        """

        return headword in self._records

    def get(
        self,
        headword: str,
    ) -> tuple[
        CanonicalLexicalRecord,
        ...
    ]:
        """
        Returns all canonical records for one headword.
        """

        return tuple(

            self._records.get(
                headword,
                [],
            )

        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    @property
    def headwords(
        self,
    ) -> tuple[
        str,
        ...
    ]:
        """
        All known headwords.
        """

        return tuple(

            sorted(
                self._records.keys(),
            )

        )

    @property
    def records(
        self,
    ) -> tuple[
        CanonicalLexicalRecord,
        ...
    ]:
        """
        Flat collection of all lexical records.
        """

        collection: list[
            CanonicalLexicalRecord,
        ] = []

        for values in self._records.values():

            collection.extend(
                values,
            )

        return tuple(
            collection,
        )

    @property
    def headword_count(
        self,
    ) -> int:
        """
        Number of unique headwords.
        """

        return len(
            self._records,
        )

    @property
    def record_count(
        self,
    ) -> int:
        """
        Number of lexical records.
        """

        return len(
            self.records,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Repository summary.
        """

        return {

            "repository": self.__class__.__name__,

            "unique_headwords": self.headword_count,

            "records": self.record_count,

        }

    # ---------------------------------------------------------
    # Python Protocol
    # ---------------------------------------------------------

    def __contains__(
        self,
        headword: str,
    ) -> bool:

        return self.contains(
            headword,
        )

    def __len__(
        self,
    ) -> int:

        return self.record_count

    def __iter__(
        self,
    ):

        yield from self.records

    def __str__(
        self,
    ) -> str:

        return (
            "CanonicalLexicalRepository("
            f"{self.headword_count} headwords, "
            f"{self.record_count} records)"
        )
