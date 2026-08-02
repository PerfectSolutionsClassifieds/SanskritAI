from __future__ import annotations

"""
SanskritAI
==========

Canonical Etymology

Purpose
-------
Represents the etymological derivation of a Sanskrit
lexical item.

Unlike Dictionary Senses, which are contextual,
CanonicalEtymology describes the historical and
grammatical origin of a word.

A single lexical entry may possess multiple competing
etymologies originating from different grammatical
traditions or lexicographical authorities.

Architecture
------------

CanonicalLemma
        │
        ▼
CanonicalDictionaryEntry
        │
        ├────────────► CanonicalEtymology
        │
        ├────────────► CanonicalReference
        │
        └────────────► CanonicalDictionarySense

Examples
--------

भाषा

    √भाष् + घञ्

अग्नि

    Competing traditional derivations

गच्छति

    √गम् + लट् + तिप्

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping

from SanskritAI.acquisition.knowledge.models.canonical_reference import (
    CanonicalReference,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalEtymology:
    """
    Canonical etymological description.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    etymology_id: str

    entry_headword: str

    # ---------------------------------------------------------
    # Root Information
    # ---------------------------------------------------------

    dhatu: str | None = None

    upasarga: str | None = None

    pratyaya: str | None = None

    unadi_suffix: str | None = None

    gana: str | None = None

    # ---------------------------------------------------------
    # Derivation
    # ---------------------------------------------------------

    derivation: str | None = None

    explanation: str | None = None

    source_tradition: str | None = None

    # ---------------------------------------------------------
    # References
    # ---------------------------------------------------------

    references: tuple[
        CanonicalReference,
        ...
    ] = ()

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def has_dhatu(
        self,
    ) -> bool:

        return self.dhatu is not None

    @property
    def has_pratyaya(
        self,
    ) -> bool:

        return self.pratyaya is not None

    @property
    def reference_count(
        self,
    ) -> int:

        return len(
            self.references,
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "headword": self.entry_headword,

            "dhatu": self.dhatu,

            "pratyaya": self.pratyaya,

            "tradition": self.source_tradition,

            "references": self.reference_count,

        }

    def __str__(
        self,
    ) -> str:

        return (

            "CanonicalEtymology("

            f"{self.entry_headword}"

            ")"

        )
