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
particular textual or lexical context.

This design naturally supports multiple meanings for the
same Sanskrit word across

    • Purāṇas

    • Chapters

    • Ślokas

    • Dictionaries

without duplicating the lexical entry itself.

Architecture
------------

CanonicalDictionaryEntry
            │
            ├─────────────► Sense 1
            │
            ├─────────────► Sense 2
            │
            ├─────────────► Sense 3
            │
            ▼

Reader UI

AI Retrieval

Grammar Engine

Future Context Dictionaries

Examples
--------

Word

    अग्नि

may possess different senses

    • physical fire

    • sacrificial fire

    • deity Agni

    • digestive fire

    • spiritual radiance

Each becomes one CanonicalDictionarySense.

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping


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
    # Context
    # ---------------------------------------------------------

    corpus: str | None = None

    work: str | None = None

    section: str | None = None

    chapter: str | None = None

    verse: str | None = None

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

    source_name: str = ""

    source_version: str = ""

    citation: str | None = None

    confidence: float = 1.0

    # ---------------------------------------------------------
    # Extension Metadata
    # ---------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

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

            "corpus": self.corpus,

            "work": self.work,

            "chapter": self.chapter,

            "verse": self.verse,

            "source": self.source_name,

        }

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_contextual(
        self,
    ) -> bool:
        """
        Returns True if this sense belongs to a
        specific textual context.
        """

        return any(

            value is not None

            for value in (

                self.corpus,

                self.work,

                self.chapter,

                self.verse,

            )

        )

    @property
    def has_grammar(
        self,
    ) -> bool:
        """
        Returns True if grammatical annotations
        are available.
        """

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

    def __str__(
        self,
    ) -> str:

        return (

            "CanonicalDictionarySense("

            f"{self.entry_headword}"

            f": {self.definition})"

        )
