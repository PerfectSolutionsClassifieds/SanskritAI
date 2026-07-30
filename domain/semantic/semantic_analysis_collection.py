from __future__ import annotations

"""
SanskritAI
==========

Semantic Analysis Collection

Immutable collection of SemanticAnalysis objects.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.semantic.semantic_analysis import SemanticAnalysis


@dataclass(frozen=True, slots=True)
class SemanticAnalysisCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of semantic analyses.
    """

    analyses: tuple[SemanticAnalysis, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Semantic Analyses"

    @property
    def display_text(self) -> str:
        return f"{len(self.analyses)} analyses"

    @property
    def display_description(self) -> str:
        return "Immutable collection of semantic analyses."

    @property
    def count(self) -> int:
        return len(self.analyses)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> SemanticAnalysis | None:
        if self.is_empty:
            return None
        return self.analyses[0]

    def add(self, analysis: SemanticAnalysis) -> "SemanticAnalysisCollection":
        return SemanticAnalysisCollection(
            analyses=self.analyses + (analysis,)
        )

    def extend(
        self,
        other: "SemanticAnalysisCollection",
    ) -> "SemanticAnalysisCollection":
        return SemanticAnalysisCollection(
            analyses=self.analyses + other.analyses
        )

    def __iter__(self) -> Iterator[SemanticAnalysis]:
        return iter(self.analyses)

    def __len__(self) -> int:
        return len(self.analyses)

    def __getitem__(self, index: int) -> SemanticAnalysis:
        return self.analyses[index]

    def __str__(self) -> str:
        return self.display_text
