from __future__ import annotations

"""
SanskritAI
==========

Canonical Context

Purpose
-------
Represents the textual context in which a lexical sense
occurs.

A Context is intentionally independent of the lexical
objects themselves.

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

        ▼

CanonicalContext

Examples
--------

Śiva Purāṇa
    Rudra Saṁhitā
        Chapter 12
            Śloka 17

Bhāgavata Purāṇa
    Skandha 10
        Chapter 29
            Śloka 4

The same Sanskrit word may therefore possess different
Dictionary Senses because they reference different
CanonicalContext objects.

Version
-------
1.0.0
"""

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalContext:
    """
    Canonical textual context.
    """

    # ---------------------------------------------------------
    # Corpus
    # ---------------------------------------------------------

    corpus: str

    work: str | None = None

    section: str | None = None

    chapter: str | None = None

    chapter_title: str | None = None

    verse: str | None = None

    # ---------------------------------------------------------
    # Optional Reader Metadata
    # ---------------------------------------------------------

    page_number: int | None = None

    page_image: str | None = None

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:

        parts = [

            self.corpus,

            self.work,

            self.section,

            self.chapter,

            self.verse,

        ]

        return ":".join(

            str(part)

            for part in parts

            if part is not None

        )

    def summary(
        self,
    ) -> dict:

        return {

            "corpus": self.corpus,

            "work": self.work,

            "section": self.section,

            "chapter": self.chapter,

            "verse": self.verse,

        }

    def __str__(
        self,
    ) -> str:

        return (
            f"CanonicalContext("
            f"{self.identifier})"
        )
