
from __future__ import annotations

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

    etymology_id: str

    entry_headword: str

    dhatu: str | None = None
    upasarga: str | None = None
    pratyaya: str | None = None
    unadi_suffix: str | None = None
    gana: str | None = None

    derivation: str | None = None
    explanation: str | None = None

    source_tradition: str | None = None

    references: tuple[
        CanonicalReference,
        ...
    ] = ()

    metadata: Mapping[str, Any] = field(
        default_factory=dict,
    )

    @property
    def has_dhatu(self) -> bool:
        return self.dhatu is not None

    @property
    def has_pratyaya(self) -> bool:
        return self.pratyaya is not None

    @property
    def reference_count(self) -> int:
        return len(self.references)

    def summary(self) -> dict:
        return {
            "headword": self.entry_headword,
            "dhatu": self.dhatu,
            "pratyaya": self.pratyaya,
            "tradition": self.source_tradition,
            "references": self.reference_count,
        }

    def __str__(self) -> str:
        return (
            "CanonicalEtymology("
            f"{self.entry_headword}"
            ")"
        )
