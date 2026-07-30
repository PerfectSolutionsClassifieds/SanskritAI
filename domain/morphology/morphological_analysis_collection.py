from __future__ import annotations

"""
SanskritAI
==========

Morphological Analysis Collection

Defines the immutable ordered collection of MorphologicalAnalysis
objects.

This collection preserves analysis order so ranked analyses can
be represented naturally.

Relationship
------------

MorphologicalAnalysis
        │
        ▼
MorphologicalAnalysisCollection
        │
        ▼
MorphologicalAnalyzer

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.morphology.morphological_analysis import (
    MorphologicalAnalysis,
)


@dataclass(frozen=True, slots=True)
class MorphologicalAnalysisCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of morphological analyses.
    """

    analyses: tuple[MorphologicalAnalysis, ...] = field(
        default_factory=tuple,
    )

    @property
    def display_name(self) -> str:
        return "Morphological Analyses"

    @property
    def display_text(self) -> str:
        return f"{len(self.analyses)} Analyses"

    @property
    def display_description(self) -> str:
        return "Immutable ordered collection of morphological analyses."

    @property
    def is_empty(self) -> bool:
        return len(self.analyses) == 0

    @property
    def count(self) -> int:
        return len(self.analyses)

    @property
    def has_analyses(self) -> bool:
        return not self.is_empty

    def add(
        self,
        analysis: MorphologicalAnalysis,
    ) -> "MorphologicalAnalysisCollection":
        """
        Returns a new collection with the supplied analysis appended.
        """
        return MorphologicalAnalysisCollection(
            analyses=self.analyses + (analysis,),
        )

    def extend(
        self,
        other: "MorphologicalAnalysisCollection",
    ) -> "MorphologicalAnalysisCollection":
        """
        Returns a new collection containing all analyses from both collections.
        """
        return MorphologicalAnalysisCollection(
            analyses=self.analyses + other.analyses,
        )

    def __iter__(self) -> Iterator[MorphologicalAnalysis]:
        return iter(self.analyses)

    def __len__(self) -> int:
        return len(self.analyses)

    def __getitem__(
        self,
        index: int,
    ) -> MorphologicalAnalysis:
        return self.analyses[index]

    def __str__(self) -> str:
        return self.display_text
