from __future__ import annotations

"""
SanskritAI
==========

Monier–Williams Parser

Purpose
-------
Parses the raw Monier–Williams Sanskrit Dictionary source into
immutable RawLexicalEntry objects.

The parser performs only structural extraction.

It intentionally DOES NOT

    • normalize

    • infer grammar

    • merge entries

    • create canonical lexemes

Those responsibilities belong to later pipeline stages.

Pipeline
--------

Raw Source

        ↓

MonierWilliamsParser

        ↓

RawLexicalEntry

        ↓

MonierWilliamsTransformer

Version
-------
1.0.0
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from typing import Iterator

from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)


@dataclass(slots=True)
class MonierWilliamsParser:
    """
    Structural parser for Monier–Williams.

    This implementation establishes the parser
    architecture.

    The actual MW parsing rules will be expanded
    incrementally once the source format has been
    finalized.
    """

    source_name: str = "Monier-Williams"

    source_version: str = "unknown"

    encoding: str = "utf-8"

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def parse(
        self,
        source: Path,
    ) -> tuple[RawLexicalEntry, ...]:
        """
        Parses an acquired MW resource.

        Returns
        -------
        tuple[RawLexicalEntry, ...]

        One RawLexicalEntry for every extracted
        dictionary record.
        """

        entries: list[RawLexicalEntry] = []

        for record in self.iter_records(
            source,
        ):

            entry = self.parse_record(
                record,
            )

            if entry is not None:

                entries.append(
                    entry,
                )

        return tuple(
            entries,
        )

    # ---------------------------------------------------------
    # Record iteration
    # ---------------------------------------------------------

    def iter_records(
        self,
        source: Path,
    ) -> Iterator[str]:
        """
        Iterates over raw dictionary records.

        Current implementation:

            one line == one record

        Later implementations may parse

            XML

            HTML

            JSON

            TEI

            SQLite

            etc.
        """

        with source.open(
            "r",
            encoding=self.encoding,
        ) as stream:

            for line in stream:

                line = line.strip()

                if not line:

                    continue

                yield line

    # ---------------------------------------------------------
    # Record parsing
    # ---------------------------------------------------------

    def parse_record(
        self,
        record: str,
    ) -> RawLexicalEntry | None:
        """
        Converts one raw MW record into a
        RawLexicalEntry.

        Placeholder implementation.

        Real parsing rules will later identify

            headword

            transliteration

            entry type

            definition

            citations

            metadata
        """

        headword = self.extract_headword(
            record,
        )

        return RawLexicalEntry(

            source_name=self.source_name,

            source_version=self.source_version,

            source_record_id=headword,

            headword=headword,

            raw_text=record,

        )

    # ---------------------------------------------------------
    # Extraction helpers
    # ---------------------------------------------------------

    def extract_headword(
        self,
        record: str,
    ) -> str:
        """
        Extracts the dictionary headword.

        Temporary implementation:

            first whitespace-separated token.

        This will later become a dedicated parser.
        """

        return record.split(
            maxsplit=1,
        )[0]

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Parser metadata.
        """

        return {

            "parser": self.__class__.__name__,

            "source": self.source_name,

            "version": self.source_version,

            "encoding": self.encoding,

        }

    def __str__(
        self,
    ) -> str:

        return (
            "MonierWilliamsParser("
            f"source='{self.source_name}')"
        )
