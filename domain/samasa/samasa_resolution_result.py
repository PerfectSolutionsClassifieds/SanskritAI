from __future__ import annotations

"""
SanskritAI
==========

Samasa Resolution Result

Canonical output produced by the Samasa Resolution Kernel.

Relationship
------------

ResolutionContext
        │
        ▼
SamasaResolutionStage
        │
        ▼
SamasaService
        │
        ▼
SamasaResolutionResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)

from SanskritAI.domain.samasa.samasa_analysis_collection import (
    SamasaAnalysisCollection,
)


@dataclass(frozen=True, slots=True)
class SamasaResolutionResult(
    ResolutionResult,
):
    """
    Canonical result produced by the Samasa Kernel.
    """

    analyses: SamasaAnalysisCollection = field(
        default_factory=SamasaAnalysisCollection,
    )

    diagnostics: tuple[
        ResolutionDiagnostic,
        ...
    ] = field(default_factory=tuple)

    confidence: float = 1.0

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Samasa Resolution Result"

    @property
    def display_text(self) -> str:
        return (
            f"{self.context.subject}"
            f" → {self.analyses.display_text}"
        )

    @property
    def display_description(self) -> str:
        return (
            "Canonical Samasa resolution result."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def result(self) -> SamasaAnalysisCollection:
        return self.analyses

    @property
    def has_analyses(self) -> bool:
        return self.analyses.has_analyses

    @property
    def analysis_count(self) -> int:
        return self.analyses.count

    @property
    def succeeded(self) -> bool:
        return self.has_analyses

    def __str__(self) -> str:
        return self.display_text
