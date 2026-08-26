from __future__ import annotations

"""
SanskritAI
==========

Sandhi Analysis Collection

Defines the immutable ordered collection of SandhiAnalysis
objects.

The collection preserves analysis order so ranked Sandhi
outputs can be represented naturally.

Relationship
------------

SandhiAnalysis
       │
       ▼
SandhiAnalysisCollection
       │
       ▼
SandhiResolutionResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.sandhi.sandhi_analysis import (
    SandhiAnalysis,
)


@dataclass(frozen=True, slots=True)
class SandhiAnalysisCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of Sandhi analyses.
    """

    analyses: tuple[SandhiAnalysis, ...] = field(
        default_factory=tuple,
    )

    @property
    def display_name(self) -> str:
        return "Sandhi Analyses"

    @property
    def display_text(self) -> str:
        return f"{len(self.analyses)} Analyses"

    @property
    def display_description(self) -> str:
        return (
            "Immutable ordered collection of Sandhi analyses."
        )

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
    def first(self) -> SandhiAnalysis | None:
        if self.is_empty:
            return None

        return self.analyses[0]

    @property
    def last(self) -> SandhiAnalysis | None:
        if self.is_empty:
            return None

        return self.analyses[-1]

    def add(
        self,
        analysis: SandhiAnalysis,
    ) -> "SandhiAnalysisCollection":
        """
        Return a new collection with the supplied analysis
        appended.

        The existing collection remains unchanged.
        """

        return SandhiAnalysisCollection(
            analyses=self.analyses + (analysis,),
        )

    def extend(
        self,
        other: "SandhiAnalysisCollection",
    ) -> "SandhiAnalysisCollection":
        """
        Return a new collection containing analyses from
        both collections.
        """

        return SandhiAnalysisCollection(
            analyses=self.analyses + other.analyses,
        )

    def __iter__(self) -> Iterator[SandhiAnalysis]:
        return iter(self.analyses)

    def __len__(self) -> int:
        return len(self.analyses)

    def __getitem__(
        self,
        index: int,
    ) -> SandhiAnalysis:
        return self.analyses[index]

    def __str__(self) -> str:
        return self.display_text
