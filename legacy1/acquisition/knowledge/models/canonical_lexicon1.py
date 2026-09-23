from __future__ import annotations

"""
SanskritAI
==========

Canonical Lexicon

Purpose
-------
Represents one complete lexical repository.

Examples

    Monier–Williams Lexicon

    Apte Lexicon

    Amarakośa Lexicon

    Śabdakalpadruma Lexicon

    Vācaspatyam Lexicon

Later

    Śiva Purāṇa Context Dictionary

    Viṣṇu Purāṇa Context Dictionary

    Bhāgavata Context Dictionary

Each CanonicalLexicon owns

    Dictionary Entries

Each Dictionary Entry owns

    Dictionary Senses

Architecture
------------

CanonicalLexicon

        │

        ├──────────────► CanonicalDictionaryEntry

        │                       │

        │                       ├────────► Sense

        │                       ├────────► Sense

        │                       └────────► Sense

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Mapping

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalLexicon:
    """
    Canonical lexical repository.
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

    def summary(
        self,
    ) -> dict:

        return {

            "identifier": self.identifier,

            "name": self.name,

            "version": self.version,

            "entries": self.entry_count,

        }

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
            f"CanonicalLexicon("
            f"{self.name}, "
            f"{self.entry_count} entries)"
        )
