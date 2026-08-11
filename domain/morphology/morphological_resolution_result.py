from __future__ import annotations

"""
SanskritAI
==========

Morphological Resolution Result

Purpose
-------
Represents the outcome of the Morphology Kernel.

Unlike MorphologicalAnalysis, which represents one candidate
analysis, this class represents the complete resolution process.

Hierarchy
---------

ResolutionResult
        │
        ▼
MorphologicalResolutionResult
        │
        ├── MorphologicalAnalysis
        ├── MorphologicalAnalysisCollection
        └── Preferred Analysis

Version
-------
v2.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.morphology.morphological_analysis import (
    MorphologicalAnalysis,
)

from SanskritAI.domain.morphology.morphological_analysis_collection import (
    MorphologicalAnalysisCollection,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MorphologicalResolutionResult(
    ResolutionResult,
):
    """
    Result produced by the Morphology Kernel.
    """

    preferred_analysis: MorphologicalAnalysis | None = None

    analyses: MorphologicalAnalysisCollection = (
        MorphologicalAnalysisCollection()
    )

    ambiguity_detected: bool = False

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    @property
    def has_analysis(
        self,
    ) -> bool:

        return self.preferred_analysis is not None

    @property
    def analysis(
        self,
    ) -> MorphologicalAnalysis | None:

        return self.preferred_analysis

    @property
    def analysis_count(
        self,
    ) -> int:

        return self.analyses.count

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    @property
    def resolved(
        self,
    ) -> bool:

        return (
            self.succeeded
            and self.has_analysis
        )

    @property
    def unresolved(
        self,
    ) -> bool:

        return not self.resolved

    @property
    def is_unique(
        self,
    ) -> bool:

        return (
            self.resolved
            and not self.ambiguity_detected
        )

    @property
    def is_ambiguous(
        self,
    ) -> bool:

        return self.ambiguity_detected

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def features(
        self,
    ):

        if self.preferred_analysis is None:
            return None

        return self.preferred_analysis.features

    @property
    def word_form(
        self,
    ):

        if self.preferred_analysis is None:
            return None

        return self.preferred_analysis.word_form

    @property
    def is_nominal(
        self,
    ) -> bool:

        if self.features is None:
            return False

        return self.features.is_nominal

    @property
    def is_verbal(
        self,
    ) -> bool:

        if self.features is None:
            return False

        return self.features.is_verbal

    @property
    def is_indeclinable(
        self,
    ) -> bool:

        if self.features is None:
            return False

        return self.features.is_indeclinable

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Morphological Resolution Result"

    @property
    def display_text(
        self,
    ) -> str:

        if self.unresolved:
            return "No morphological resolution"

        return self.preferred_analysis.display_text

    @property
    def display_description(
        self,
    ) -> str:

        if self.unresolved:
            return self.display_text

        return (
            f"{self.analysis_count} candidate analysis"
            f"{'' if self.analysis_count == 1 else 'es'}"
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text
