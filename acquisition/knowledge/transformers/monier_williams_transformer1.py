from __future__ import annotations

"""
SanskritAI
==========

Monier–Williams Transformer

Purpose
-------
Transforms RawLexicalEntry objects extracted from the
Monier–Williams dictionary into the canonical lexical
representation used throughout SanskritAI.

The transformer performs the FIRST semantic normalization
layer while deliberately avoiding grammatical inference.

Pipeline
--------

RawLexicalEntry
        │
        ▼
MonierWilliamsTransformer
        │
        ▼
Canonical Lexical Record
        │
        ▼
Lexical Repository
        │
        ▼
Reader UI
        │
        ▼
AI Modules

Design Principles
-----------------

• Deterministic

• Pure transformation

• No I/O

• No database writes

• No parser logic

• Preserve provenance

Version
-------
1.0.0
"""

from dataclasses import dataclass
from typing import Iterable

from SanskritAI.acquisition.knowledge.models.raw_lexical_entry import (
    RawLexicalEntry,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalLexicalRecord:
    """
    Canonical intermediate lexical representation.

    This object is intentionally generic so that every
    lexical resource (MW, Apte, Amarakośa,
    Śabdakalpadruma, etc.) can transform into the same
    schema before repository insertion.
    """

    headword: str

    transliteration: str | None

    language: str

    script: str

    definition: str

    entry_type: str | None

    source_name: str

    source_version: str

    source_record_id: str

    citation: str | None

    metadata: dict


@dataclass(slots=True)
class MonierWilliamsTransformer:
    """
    Canonical transformer for Monier–Williams.
    """

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def transform(
        self,
        entry: RawLexicalEntry,
    ) -> CanonicalLexicalRecord:
        """
        Converts one RawLexicalEntry into the canonical
        lexical representation.
        """

        return CanonicalLexicalRecord(

            headword=entry.headword.strip(),

            transliteration=entry.transliteration,

            language=entry.language,

            script=entry.script,

            definition=entry.raw_text.strip(),

            entry_type=entry.entry_type,

            source_name=entry.source_name,

            source_version=entry.source_version,

            source_record_id=entry.source_record_id,

            citation=entry.citation,

            metadata=dict(
                entry.metadata,
            ),
        )

    # ---------------------------------------------------------
    # Batch transformation
    # ---------------------------------------------------------

    def transform_all(
        self,
        entries: Iterable[
            RawLexicalEntry,
        ],
    ) -> tuple[
        CanonicalLexicalRecord,
        ...
    ]:
        """
        Transforms multiple entries.
        """

        return tuple(

            self.transform(
                entry,
            )

            for entry in entries

        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:
        """
        Transformer metadata.
        """

        return {

            "transformer": self.__class__.__name__,

            "target": "CanonicalLexicalRecord",

            "resource": "Monier-Williams",

        }

    def __str__(
        self,
    ) -> str:

        return (
            "MonierWilliamsTransformer("
            "CanonicalLexicalRecord)"
        )
