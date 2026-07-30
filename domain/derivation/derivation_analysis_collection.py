from __future__ import annotations

"""
SanskritAI
==========

Derivation Analysis Collection

Immutable collection of DerivationAnalysis objects.

This mirrors the design used by Dhatu, Pratyaya, Samasa,
Grammar and Morphology kernels.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.derivation.derivation_analysis import (
    DerivationAnalysis,
)


@dataclass(frozen=True, slots=True)
class DerivationAnalysisCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of derivation analyses.
    """

    analyses: tuple[DerivationAnalysis, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Derivation Analyses"

    @property
    def display_text(self) -> str:
        return f"{len(self.analyses)} analyses"

    @property
    def display_description(self) -> str:
        return "Immutable collection of derivation analyses."

    @property
    def count(self) -> int:
        return len(self.analyses)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> DerivationAnalysis | None:
        if self.is_empty:
            return None
        return self.analyses[0]

    def add(
        self,
        analysis: DerivationAnalysis,
    ) -> "DerivationAnalysisCollection":
        return DerivationAnalysisCollection(
            analyses=self.analyses + (analysis,)
        )

    def extend(
        self,
        other: "DerivationAnalysisCollection",
    ) -> "DerivationAnalysisCollection":
        return DerivationAnalysisCollection(
            analyses=self.analyses + other.analyses
        )

    def __iter__(self) -> Iterator[DerivationAnalysis]:
        return iter(self.analyses)

    def __len__(self) -> int:
        return len(self.analyses)

    def __getitem__(self, index: int) -> DerivationAnalysis:
        return self.analyses[index]

    def __str__(self) -> str:
        return self.display_text
