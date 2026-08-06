from __future__ import annotations

"""
SanskritAI
==========

Sandhi Resolution Result

Canonical output produced by the Sandhi Resolution Kernel.

This class specializes ResolutionResult for Sandhi analysis.

Relationship
------------

ResolutionContext
        │
        ▼
SandhiResolutionStage
        │
        ▼
SandhiService
        │
        ▼
SandhiResolutionResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)

from SanskritAI.domain.sandhi.sandhi_analysis_collection import (
    SandhiAnalysisCollection,
)


@dataclass(frozen=True, slots=True)
class SandhiResolutionResult(
    ResolutionResult,
):
    """
    Canonical result produced by the Sandhi Kernel.
    """

    analyses: SandhiAnalysisCollection = field(
        default_factory=SandhiAnalysisCollection,
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
        return "Sandhi Resolution Result"

    @property
    def display_text(self) -> str:
        return (
            f"{self.context.subject}"
            f" → {self.analyses.display_text}"
        )

    @property
    def display_description(self) -> str:
        return (
            "Canonical Sandhi resolution result."
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def result(self) -> SandhiAnalysisCollection:
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
