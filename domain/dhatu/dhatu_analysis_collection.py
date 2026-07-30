from __future__ import annotations

"""
SanskritAI
==========

Dhatu Analysis Collection

Immutable collection of DhatuAnalysis objects.

This mirrors the Morphology, Grammar and Samasa kernels.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.dhatu.dhatu_analysis import DhatuAnalysis


@dataclass(frozen=True, slots=True)
class DhatuAnalysisCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    analyses: tuple[
        DhatuAnalysis,
        ...
    ] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Dhatu Analyses"

    @property
    def display_text(self) -> str:
        return f"{len(self.analyses)} analyses"

    @property
    def display_description(self) -> str:
        return "Immutable collection of Dhatu analyses."

    @property
    def count(self) -> int:
        return len(self.analyses)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> DhatuAnalysis | None:
        if self.is_empty:
            return None
        return self.analyses[0]

    def add(
        self,
        analysis: DhatuAnalysis,
    ) -> "DhatuAnalysisCollection":

        return DhatuAnalysisCollection(
            analyses=self.analyses + (analysis,)
        )

    def extend(
        self,
        other: "DhatuAnalysisCollection",
    ) -> "DhatuAnalysisCollection":

        return DhatuAnalysisCollection(
            analyses=self.analyses + other.analyses
        )

    def __len__(self):
        return len(self.analyses)

    def __iter__(self) -> Iterator[DhatuAnalysis]:
        return iter(self.analyses)

    def __getitem__(self, index):
        return self.analyses[index]

    def __str__(self):
        return self.display_text
