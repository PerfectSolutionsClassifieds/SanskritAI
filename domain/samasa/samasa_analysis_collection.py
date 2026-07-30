from __future__ import annotations

"""
SanskritAI
==========

Samasa Analysis Collection

Defines the immutable ordered collection of SamasaAnalysis
objects.

This collection preserves analysis order so ranked compound
outputs can be represented naturally.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.samasa.samasa_analysis import SamasaAnalysis


@dataclass(frozen=True, slots=True)
class SamasaAnalysisCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of Samasa analyses.
    """

    analyses: tuple[SamasaAnalysis, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Samasa Analyses"

    @property
    def display_text(self) -> str:
        return f"{len(self.analyses)} Analyses"

    @property
    def display_description(self) -> str:
        return "Immutable ordered collection of Samasa analyses."

    @property
    def is_empty(self) -> bool:
        return len(self.analyses) == 0

    @property
    def count(self) -> int:
        return len(self.analyses)

    @property
    def has_analyses(self) -> bool:
        return not self.is_empty

    @property
    def first(self) -> SamasaAnalysis | None:
        if self.is_empty:
            return None
        return self.analyses[0]

    @property
    def last(self) -> SamasaAnalysis | None:
        if self.is_empty:
            return None
        return self.analyses[-1]

    def add(
        self,
        analysis: SamasaAnalysis,
    ) -> "SamasaAnalysisCollection":
        """
        Returns a new collection with the supplied analysis appended.
        """
        return SamasaAnalysisCollection(
            analyses=self.analyses + (analysis,),
        )

    def extend(
        self,
        other: "SamasaAnalysisCollection",
    ) -> "SamasaAnalysisCollection":
        """
        Returns a new collection containing analyses from both collections.
        """
        return SamasaAnalysisCollection(
            analyses=self.analyses + other.analyses,
        )

    def __iter__(self) -> Iterator[SamasaAnalysis]:
        return iter(self.analyses)

    def __len__(self) -> int:
        return len(self.analyses)

    def __getitem__(self, index: int) -> SamasaAnalysis:
        return self.analyses[index]

    def __str__(self) -> str:
        return self.display_text
