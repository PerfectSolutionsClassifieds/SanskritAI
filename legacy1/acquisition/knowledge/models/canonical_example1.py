from __future__ import annotations

"""
SanskritAI
==========

Canonical Example

Purpose
-------
Represents an authentic textual usage of a lexical sense.

Unlike a Dictionary Sense, which describes meaning,
a CanonicalExample demonstrates that meaning through an
actual occurrence in Sanskrit literature.

Examples may originate from

    • Purāṇas
    • Vedas
    • Upaniṣads
    • Itihāsas
    • Kāvyas
    • Amarakośa
    • Monier–Williams
    • Apte
    • Śabdakalpadruma
    • Vācaspatyam

Architecture
------------

CanonicalDictionarySense
            │
            ▼
CanonicalExample
            │
            ├────────► CanonicalContext
            │
            └────────► CanonicalReference

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)

from SanskritAI.acquisition.knowledge.models.canonical_reference import (
    CanonicalReference,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CanonicalExample:
    """
    Canonical textual example illustrating one lexical sense.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    example_id: str

    entry_headword: str

    sense_id: str

    # ---------------------------------------------------------
    # Sanskrit Example
    # ---------------------------------------------------------

    sanskrit_text: str

    transliteration: str | None = None

    translation: str | None = None

    explanation: str | None = None

    # ---------------------------------------------------------
    # Context
    # ---------------------------------------------------------

    context: CanonicalContext | None = None

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
    def has_translation(
        self,
    ) -> bool:

        return self.translation is not None

    @property
    def has_context(
        self,
    ) -> bool:

        return self.context is not None

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

            "example_id": self.example_id,

            "headword": self.entry_headword,

            "sense_id": self.sense_id,

            "references": self.reference_count,

            "has_context": self.has_context,

        }

    def __str__(
        self,
    ) -> str:

        return (
            "CanonicalExample("
            f"{self.entry_headword})"
        )
