from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Resolution Strategy

Canonical implementation of the MorphologicalResolutionStrategy.

Responsibilities
----------------

• receive MorphologicalResolutionContext

• invoke MorphologicalAnalyzer

• convert MorphologicalAnalysisCollection into
  MorphologicalResolutionResult

This class intentionally contains no grammatical rules.
All linguistic work belongs to the MorphologicalAnalyzer.

Architecture
------------

MorphologicalResolutionContext
            │
            ▼
DefaultMorphologicalResolutionStrategy
            │
            ▼
MorphologicalAnalyzer
            │
            ▼
MorphologicalAnalysisCollection
            │
            ▼
MorphologicalResolutionResult

Version
-------
v2.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.domain.morphology.default_morphological_analyzer import (
    DefaultMorphologicalAnalyzer,
)

from SanskritAI.domain.morphology.morphological_analyzer import (
    MorphologicalAnalyzer,
)

from SanskritAI.domain.morphology.morphological_resolution_context import (
    MorphologicalResolutionContext,
)

from SanskritAI.domain.morphology.morphological_resolution_result import (
    MorphologicalResolutionResult,
)

from SanskritAI.domain.morphology.morphological_resolution_strategy import (
    MorphologicalResolutionStrategy,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultMorphologicalResolutionStrategy(
    MorphologicalResolutionStrategy,
):
    """
    Canonical morphology resolution strategy.
    """

    analyzer: MorphologicalAnalyzer = field(
        default_factory=DefaultMorphologicalAnalyzer,
    )

    @property
    def display_name(
        self,
    ) -> str:
        return "Default Morphological Resolution Strategy"

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Resolves morphology using the configured "
            "MorphologicalAnalyzer."
        )

    def resolve(
        self,
        context: MorphologicalResolutionContext,
    ) -> MorphologicalResolutionResult:
        """
        Resolves morphology for the supplied lexical result.
        """

        analyses = self.analyzer.analyze(
            context.word_form,
        )

        primary = (
            analyses[0]
            if analyses.count > 0
            else None
        )

        return MorphologicalResolutionResult(
            context=context,
            analyses=analyses,
            primary_analysis=primary,
            succeeded=primary is not None,
            confidence=(
                primary.confidence
                if primary is not None
                else 0.0
            ),
        )
