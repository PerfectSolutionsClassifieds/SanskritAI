from __future__ import annotations

"""
SanskritAI
==========

Vakya Analysis Collection

Immutable collection of VakyaAnalysis objects.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.vakya.vakya_analysis import VakyaAnalysis


@dataclass(frozen=True, slots=True)
class VakyaAnalysisCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of sentence analyses.
    """

    analyses: tuple[VakyaAnalysis, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Vakya Analyses"

    @property
    def display_text(self) -> str:
        return f"{len(self.analyses)} analyses"

    @property
    def display_description(self) -> str:
        return "Immutable collection of sentence analyses."

    @property
    def count(self) -> int:
        return len(self.analyses)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> VakyaAnalysis | None:
        if self.is_empty:
            return None
        return self.analyses[0]

    def add(self, analysis: VakyaAnalysis) -> "VakyaAnalysisCollection":
        return VakyaAnalysisCollection(
            analyses=self.analyses + (analysis,)
        )

    def extend(
        self,
        other: "VakyaAnalysisCollection",
    ) -> "VakyaAnalysisCollection":
        return VakyaAnalysisCollection(
            analyses=self.analyses + other.analyses
        )

    def __iter__(self) -> Iterator[VakyaAnalysis]:
        return iter(self.analyses)

    def __len__(self) -> int:
        return len(self.analyses)

    def __getitem__(self, index: int) -> VakyaAnalysis:
        return self.analyses[index]

    def __str__(self) -> str:
        return self.display_text
