
from __future__ import annotations

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

    example_id: str
    entry_headword: str
    sense_id: str

    sanskrit_text: str

    transliteration: str | None = None
    translation: str | None = None
    explanation: str | None = None

    context: CanonicalContext | None = None

    references: tuple[
        CanonicalReference,
        ...
    ] = ()

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    @property
    def has_translation(self) -> bool:
        return self.translation is not None

    @property
    def has_context(self) -> bool:
        return self.context is not None

    @property
    def reference_count(self) -> int:
        return len(self.references)

    def summary(self) -> dict:
        return {
            "example_id": self.example_id,
            "headword": self.entry_headword,
            "sense_id": self.sense_id,
            "references": self.reference_count,
            "has_context": self.has_context,
        }

    def __str__(self) -> str:
        return (
            "CanonicalExample("
            f"{self.entry_headword})"
        )
