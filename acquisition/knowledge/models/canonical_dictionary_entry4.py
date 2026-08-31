
from __future__ import annotations

"""
SanskritAI
==========

Canonical Dictionary Entry

Purpose
-------
Immutable canonical lexical entry.

A CanonicalDictionaryEntry represents the lexical identity
of a Sanskrit headword.

Senses are supplied at construction time and are immutable.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)

from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalDictionaryEntry:
    """
    Immutable canonical lexical entry.
    """

    headword: str

    transliteration: str | None = None
    language: str = "sa"
    script: str = "Devanagari"

    lemma: CanonicalLemma | None = None

    normalized_headword: str | None = None
    entry_type: str | None = None

    senses: tuple[
        CanonicalDictionarySense,
        ...,
    ] = ()

    source_name: str = ""
    source_version: str = ""
    source_record_id: str = ""

    citation: str | None = None

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    # =========================================================
    # Properties
    # =========================================================

    @property
    def sense_count(self) -> int:
        return len(self.senses)

    @property
    def display_name(self) -> str:
        return self.headword

    @property
    def has_transliteration(self) -> bool:
        return self.transliteration is not None

    @property
    def has_multiple_senses(self) -> bool:
        return self.sense_count > 1

    # =========================================================
    # Sense Access
    # =========================================================

    def primary_sense(
        self,
    ) -> CanonicalDictionarySense | None:
        if not self.senses:
            return None

        return self.senses[0]

    # =========================================================
    # Summary
    # =========================================================

    def summary(self) -> dict[str, Any]:
        return {
            "headword": self.headword,
            "lemma": (
                None
                if self.lemma is None
                else self.lemma.lemma
            ),
            "source": self.source_name,
            "entry_type": self.entry_type,
            "sense_count": self.sense_count,
        }

    # =========================================================
    # Python Protocol
    # =========================================================

    def __len__(self) -> int:
        return self.sense_count

    def __iter__(self):
        yield from self.senses

    def __str__(self) -> str:
        return (
            "CanonicalDictionaryEntry("
            f"{self.headword}, "
            f"{self.sense_count} senses)"
        )
