from __future__ import annotations

"""
SanskritAI
==========

Lexical Entry Collection

Defines the immutable collection of LexicalEntry aggregate roots.

A LexicalEntryCollection represents a coherent set of lexical
concepts returned from a repository, parser, search engine,
dictionary lookup, or semantic retrieval operation.

Relationship
------------

LexicalEntry
        │
        ▼
LexicalEntryCollection
        │
        ▼
LexicalRepository
        │
        ▼
LexicalService

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.lexical.lexical_entry import (
    LexicalEntry,
)


@dataclass(frozen=True, slots=True)
class LexicalEntryCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of LexicalEntry aggregate roots.
    """

    entries: tuple[
        LexicalEntry,
        ...
    ] = field(default_factory=tuple)

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Lexical Entry Collection"

    @property
    def display_text(self) -> str:
        return f"{self.count} Lexical Entries"

    @property
    def display_description(self) -> str:
        return (
            "Immutable collection of lexical entry "
            "aggregate roots."
        )

    # ---------------------------------------------------------
    # Collection Properties
    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        return len(self.entries)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def has_entries(self) -> bool:
        return not self.is_empty

    @property
    def first(self) -> LexicalEntry | None:
        if self.is_empty:
            return None

        return self.entries[0]

    @property
    def last(self) -> LexicalEntry | None:
        if self.is_empty:
            return None

        return self.entries[-1]

    # ---------------------------------------------------------
    # Immutable Operations
    # ---------------------------------------------------------

    def add(
        self,
        entry: LexicalEntry,
    ) -> "LexicalEntryCollection":
        """
        Returns a new collection with the supplied lexical
        entry appended.
        """

        return LexicalEntryCollection(
            entries=self.entries + (entry,),
        )

    def extend(
        self,
        other: "LexicalEntryCollection",
    ) -> "LexicalEntryCollection":
        """
        Returns a new collection containing entries from both
        collections.
        """

        return LexicalEntryCollection(
            entries=self.entries + other.entries,
        )

    # ---------------------------------------------------------
    # Lookup Helpers
    # ---------------------------------------------------------

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Returns True if an entry having the supplied identifier
        exists.
        """

        return any(
            entry.identifier == identifier
            for entry in self.entries
        )

    def get(
        self,
        identifier: str,
    ) -> LexicalEntry | None:
        """
        Returns the lexical entry having the supplied
        identifier, otherwise None.
        """

        for entry in self.entries:
            if entry.identifier == identifier:
                return entry

        return None

    # ---------------------------------------------------------
    # Python Protocols
    # ---------------------------------------------------------

    def __iter__(self) -> Iterator[LexicalEntry]:
        return iter(self.entries)

    def __len__(self) -> int:
        return self.count

    def __getitem__(
        self,
        index: int,
    ) -> LexicalEntry:
        return self.entries[index]

    def __contains__(
        self,
        entry: LexicalEntry,
    ) -> bool:
        return entry in self.entries

    def __str__(self) -> str:
        return self.display_text
