from __future__ import annotations

"""
SanskritAI
==========

Canonical Lexicon

Purpose
-------
Represents one complete canonical lexical repository.

A CanonicalLexicon is the immutable root of the lexical
knowledge graph.

Architecture
------------

CanonicalLexicon
        │
        ▼
CanonicalDictionaryEntry
        │
        ▼
CanonicalDictionarySense
        │
        ├────────────► CanonicalContext
        │
        └────────────► CanonicalSource

Version
-------
2.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Mapping
from typing import Iterator

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)

from SanskritAI.acquisition.knowledge.models.canonical_source import (
    CanonicalSource,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalLexicon:
    """
    Immutable canonical lexical repository.
    """

    identifier: str

    name: str

    version: str

    language: str = "sa"

    description: str | None = None

    source: str | None = None

    entries: Mapping[
        str,
        CanonicalDictionaryEntry,
    ] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Entries
    # ---------------------------------------------------------

    @property
    def entry_count(
        self,
    ) -> int:

        return len(
            self.entries,
        )

    def contains(
        self,
        headword: str,
    ) -> bool:

        return headword in self.entries

    def get(
        self,
        headword: str,
    ) -> CanonicalDictionaryEntry | None:

        return self.entries.get(
            headword,
        )

    def all_entries(
        self,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...
    ]:

        return tuple(
            self.entries.values()
        )

    # ---------------------------------------------------------
    # Graph Traversal
    # ---------------------------------------------------------

    def all_senses(
        self,
    ) -> Iterator[
        CanonicalDictionarySense
    ]:

        for entry in self.entries.values():

            yield from entry.senses

    def all_contexts(
        self,
    ) -> Iterator[
        CanonicalContext
    ]:

        seen: set[str] = set()

        for sense in self.all_senses():

            if sense.context is None:
                continue

            identifier = sense.context.identifier

            if identifier in seen:
                continue

            seen.add(identifier)

            yield sense.context

    def all_sources(
        self,
    ) -> Iterator[
        CanonicalSource
    ]:

        seen: set[str] = set()

        for sense in self.all_senses():

            if sense.source is None:
                continue

            if sense.source.source_id in seen:
                continue

            seen.add(
                sense.source.source_id
            )

            yield sense.source

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def sense_count(
        self,
    ) -> int:

        return sum(

            len(entry)

            for entry in self.entries.values()

        )

    def summary(
        self,
    ) -> dict:

        return {

            "identifier": self.identifier,

            "name": self.name,

            "version": self.version,

            "entries": self.entry_count,

            "senses": self.sense_count,

        }

    # ---------------------------------------------------------
    # Python Protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.entry_count

    def __iter__(
        self,
    ):

        yield from self.entries.values()

    def __str__(
        self,
    ) -> str:

        return (

            "CanonicalLexicon("

            f"{self.name}, "

            f"{self.entry_count} entries, "

            f"{self.sense_count} senses)"

        )
