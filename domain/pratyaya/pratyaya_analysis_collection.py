from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Analysis Collection

Immutable collection of PratyayaAnalysis objects.

This mirrors the Morphology, Grammar, Samasa and Dhatu
kernels.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.pratyaya.pratyaya_analysis import PratyayaAnalysis


@dataclass(frozen=True, slots=True)
class PratyayaAnalysisCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    analyses: tuple[
        PratyayaAnalysis,
        ...
    ] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Pratyaya Analyses"

    @property
    def display_text(self) -> str:
        return f"{len(self.analyses)} analyses"

    @property
    def display_description(self) -> str:
        return "Immutable collection of Pratyaya analyses."

    @property
    def count(self) -> int:
        return len(self.analyses)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> PratyayaAnalysis | None:
        if self.is_empty:
            return None
        return self.analyses[0]

    def add(
        self,
        analysis: PratyayaAnalysis,
    ) -> "PratyayaAnalysisCollection":
        return PratyayaAnalysisCollection(
            analyses=self.analyses + (analysis,)
        )

    def extend(
        self,
        other: "PratyayaAnalysisCollection",
    ) -> "PratyayaAnalysisCollection":
        return PratyayaAnalysisCollection(
            analyses=self.analyses + other.analyses
        )

    def __iter__(self) -> Iterator[PratyayaAnalysis]:
        return iter(self.analyses)

    def __len__(self) -> int:
        return len(self.analyses)

    def __getitem__(self, index: int) -> PratyayaAnalysis:
        return self.analyses[index]

    def __str__(self) -> str:
        return self.display_text
