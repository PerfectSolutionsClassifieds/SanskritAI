from __future__ import annotations

"""
SanskritAI
==========

Canonical Dictionary Sense

Purpose
-------
Represents one contextual meaning (Sense) of a Sanskrit
headword.

Unlike CanonicalDictionaryEntry, which represents the
lexical identity of a word, CanonicalDictionarySense
represents one interpretation of that word within a
particular textual context.

This refactored version establishes the canonical
object graph by referencing immutable Context and
Source objects directly.

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
        ├──────────────► CanonicalContext
        │
        └──────────────► CanonicalSource

Reader UI
Grammar Engine
AI Retrieval
REST APIs

Version
-------
2.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping

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
class CanonicalDictionarySense:
    """
    Canonical contextual meaning of a lexical entry.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    sense_id: str

    entry_headword: str

    # ---------------------------------------------------------
    # Meaning
    # ---------------------------------------------------------

    definition: str

    gloss: str | None = None

    semantic_notes: str | None = None

    # ---------------------------------------------------------
    # Canonical Relationships
    # ---------------------------------------------------------

    context: CanonicalContext | None = None

    source: CanonicalSource | None = None

    # ---------------------------------------------------------
    # Linguistic Classification
    # ---------------------------------------------------------

    part_of_speech: str | None = None

    grammatical_gender: str | None = None

    grammatical_number: str | None = None

    vibhakti: str | None = None

    dhatu: str | None = None

    pratyaya: str | None = None

    samasa: str | None = None

    sandhi: str | None = None

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    citation: str | None = None

    confidence: float = 1.0

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
    def has_context(
        self,
    ) -> bool:

        return self.context is not None

    @property
    def has_source(
        self,
    ) -> bool:

        return self.source is not None

    @property
    def has_grammar(
        self,
    ) -> bool:

        return any(

            value is not None

            for value in (

                self.part_of_speech,

                self.vibhakti,

                self.dhatu,

                self.pratyaya,

                self.samasa,

                self.sandhi,

            )

        )

    @property
    def identifier(
        self,
    ) -> str:

        return self.sense_id

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "sense_id": self.sense_id,

            "headword": self.entry_headword,

            "definition": self.definition,

            "context":
                None
                if self.context is None
                else self.context.identifier,

            "source":
                None
                if self.source is None
                else self.source.display_name,

            "confidence": self.confidence,

        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        context = (
            self.context.identifier
            if self.context is not None
            else "global"
        )

        return (

            "CanonicalDictionarySense("

            f"{self.entry_headword}"

            f" @ {context}"

            ")"

        )
