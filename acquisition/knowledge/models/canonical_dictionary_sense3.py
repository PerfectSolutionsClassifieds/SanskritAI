
from __future__ import annotations

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

    sense_id: str
    entry_headword: str

    definition: str

    gloss: str | None = None
    semantic_notes: str | None = None

    context: CanonicalContext | None = None
    source: CanonicalSource | None = None

    part_of_speech: str | None = None
    grammatical_gender: str | None = None
    grammatical_number: str | None = None
    vibhakti: str | None = None

    dhatu: str | None = None
    pratyaya: str | None = None
    samasa: str | None = None
    sandhi: str | None = None

    citation: str | None = None

    confidence: float = 1.0

    metadata: Mapping[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )

    @property
    def has_context(self) -> bool:
        return self.context is not None

    @property
    def has_source(self) -> bool:
        return self.source is not None

    @property
    def has_grammar(self) -> bool:
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
    def identifier(self) -> str:
        return self.sense_id

    def summary(self) -> dict:
        return {
            "sense_id": self.sense_id,
            "headword": self.entry_headword,
            "definition": self.definition,
            "context": (
                None
                if self.context is None
                else self.context.identifier
            ),
            "source": (
                None
                if self.source is None
                else self.source.display_name
            ),
            "confidence": self.confidence,
        }

    def __str__(self) -> str:
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
