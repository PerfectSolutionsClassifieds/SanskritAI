from __future__ import annotations

"""
SanskritAI
==========

Headword Index

Purpose
-------
Provides the canonical searchable index over Sanskrit
headwords contained in the Canonical Knowledge Repository.

Unlike the registries, which merely own canonical objects,
the HeadwordIndex is responsible for efficient retrieval.

Architecture
------------

CanonicalKnowledgeRepository
            │
            ▼
      HeadwordIndex
            │
            ▼
CanonicalDictionaryEntry
            │
            ▼
CanonicalDictionarySense

Responsibilities
----------------

• Index canonical dictionary entries by headword
• Fast exact lookup
• Prefix lookup
• Enumerate indexed headwords
• Support future fuzzy lookup

Notes
-----

The HeadwordIndex intentionally does NOT perform any
grammatical reasoning.

That responsibility belongs to future components:

    LemmaIndex

    ContextIndex

    LexicalLookupEngine

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)


@dataclass(slots=True)
class HeadwordIndex:
    """
    Canonical searchable index for Sanskrit headwords.
    """

    _entries: dict[
        str,
        CanonicalDictionaryEntry,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Index Construction
    # ---------------------------------------------------------

    def add(
        self,
        entry: CanonicalDictionaryEntry,
    ) -> None:
        """
        Adds one canonical dictionary entry.
        """

        headword = entry.headword.strip()

        if not headword:
            return

        self._entries.setdefault(
            headword,
            entry,
        )

    def build(
        self,
        entries: tuple[
            CanonicalDictionaryEntry,
            ...,
        ],
    ) -> None:
        """
        Builds the index.
        """

        self.clear()

        for entry in entries:

            self.add(
                entry,
            )

    def clear(
        self,
    ) -> None:

        self._entries.clear()

    # ---------------------------------------------------------
    # Exact Lookup
    # ---------------------------------------------------------

    def lookup(
        self,
        headword: str,
    ) -> CanonicalDictionaryEntry | None:

        return self._entries.get(
            headword,
        )

    # ---------------------------------------------------------
    # Prefix Lookup
    # ---------------------------------------------------------

    def prefix_search(
        self,
        prefix: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:

        prefix = prefix.strip()

        if not prefix:
            return ()

        return tuple(

            sorted(

                (

                    entry

                    for headword, entry

                    in self._entries.items()

                    if headword.startswith(
                        prefix,
                    )

                ),

                key=lambda x: x.headword,

            )

        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all_entries(
        self,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:

        return tuple(

            sorted(

                self._entries.values(),

                key=lambda x: x.headword,

            )

        )

    @property
    def headwords(
        self,
    ) -> tuple[
        str,
        ...,
    ]:

        return tuple(

            sorted(

                self._entries.keys(),

            )

        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "indexed_entries": len(
                self,
            ),

            "headwords": len(
                self.headwords,
            ),

        }

    # ---------------------------------------------------------
    # Python Protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._entries,
        )

    def __iter__(
        self,
    ):

        yield from self.all_entries()

    def __contains__(
        self,
        headword: str,
    ) -> bool:

        return headword in self._entries

    def __str__(
        self,
    ) -> str:

        return (

            "HeadwordIndex("

            f"{len(self)} indexed entries)"

        )
