from __future__ import annotations

"""
SanskritAI
==========

Canonical Dictionary Entry

Purpose
-------
Represents one canonical Sanskrit lexical entry.

Unlike previous versions, the Dictionary Entry now owns
its contextual Dictionary Senses, making the lexical graph
fully traversable.

Architecture
------------

CanonicalLexicon
        │
        ▼
CanonicalDictionaryEntry
        │
        ├──────────────► CanonicalDictionarySense
        ├──────────────► CanonicalDictionarySense
        └──────────────► CanonicalDictionarySense

Version
-------
2.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalDictionaryEntry:
    """
    Canonical lexical entry.

    One entry represents the lexical identity of a Sanskrit
    headword.

    Contextual meanings are represented by the immutable
    CanonicalDictionarySense objects owned by this entry.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    headword: str

    transliteration: str | None = None

    # ---------------------------------------------------------
    # Language
    # ---------------------------------------------------------

    language: str = "sa"

    script: str = "Devanagari"

    # ---------------------------------------------------------
    # Lexical Metadata
    # ---------------------------------------------------------

    lemma: str | None = None

    normalized_headword: str | None = None

    entry_type: str | None = None

    # ---------------------------------------------------------
    # Contextual Meanings
    # ---------------------------------------------------------

    senses: tuple[
        CanonicalDictionarySense,
        ...
    ] = ()

    # ---------------------------------------------------------
    # Source Information
    # ---------------------------------------------------------

    source_name: str = ""

    source_version: str = ""

    source_record_id: str = ""

    citation: str | None = None

    # ---------------------------------------------------------
    # Extension Metadata
    # ---------------------------------------------------------

    metadata: Mapping[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def sense_count(
        self,
    ) -> int:

        return len(
            self.senses,
        )

    @property
    def display_name(
        self,
    ) -> str:

        return self.headword

    @property
    def has_transliteration(
        self,
    ) -> bool:

        return self.transliteration is not None

    @property
    def has_multiple_senses(
        self,
    ) -> bool:

        return self.sense_count > 1

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def primary_sense(
        self,
    ) -> CanonicalDictionarySense | None:

        if not self.senses:
            return None

        return self.senses[0]

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "headword": self.headword,

            "lemma": self.lemma,

            "source": self.source_name,

            "entry_type": self.entry_type,

            "sense_count": self.sense_count,

        }

    # ---------------------------------------------------------
    # Python Protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.sense_count

    def __iter__(
        self,
    ):

        yield from self.senses

    def __str__(
        self,
    ) -> str:

        return (
            "CanonicalDictionaryEntry("
            f"{self.headword}, "
            f"{self.sense_count} senses)"
        )
