from __future__ import annotations

"""
SanskritAI
==========

Canonical Reference

Purpose
-------
Represents an authoritative bibliographic or textual
reference associated with a lexical entry, dictionary
sense, example, or etymological statement.

A CanonicalReference is intentionally independent of any
specific lexical resource and may refer to

    • Monier–Williams
    • Apte
    • Amarakośa
    • Śabdakalpadruma
    • Vācaspatyam
    • Dhātupāṭha
    • Gaṇapāṭha
    • Uṇādi
    • Purāṇas
    • Vedas
    • Upaniṣads
    • Kāvyas
    • Commentaries

Architecture
------------

CanonicalDictionarySense
        │
        ├────────────► CanonicalReference
        │
CanonicalExample
        │
        ├────────────► CanonicalReference
        │
CanonicalEtymology
        │
        └────────────► CanonicalReference

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
class CanonicalReference:
    """
    Canonical bibliographic / textual reference.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    reference_id: str

    # ---------------------------------------------------------
    # Source
    # ---------------------------------------------------------

    source_name: str

    work: str | None = None

    section: str | None = None

    chapter: str | None = None

    verse: str | None = None

    page: str | None = None

    line: str | None = None

    edition: str | None = None

    publication_year: int | None = None

    # ---------------------------------------------------------
    # Optional Online Location
    # ---------------------------------------------------------

    url: str | None = None

    # ---------------------------------------------------------
    # Citation
    # ---------------------------------------------------------

    citation: str | None = None

    notes: str | None = None

    # ---------------------------------------------------------
    # Extension Metadata
    # ---------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def location(
        self,
    ) -> str:

        parts = [

            self.work,

            self.section,

            self.chapter,

            self.verse,

            self.page,

        ]

        return " : ".join(

            str(part)

            for part in parts

            if part is not None

        )

    def summary(
        self,
    ) -> dict:

        return {

            "source": self.source_name,

            "work": self.work,

            "chapter": self.chapter,

            "verse": self.verse,

            "page": self.page,

        }

    def __str__(
        self,
    ) -> str:

        if self.location:

            return (
                f"{self.source_name} "
                f"({self.location})"
            )

        return self.source_name
