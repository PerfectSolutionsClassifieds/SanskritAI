from __future__ import annotations

"""
SanskritAI
==========

Dhatu Result

Defines the immutable outcome produced by every Dhatu
analysis.

Unlike earlier iterations, the result no longer exposes raw
Dhatu objects. Instead it exposes a canonical
DhatuAnalysisCollection, mirroring the architecture already
established by the Morphology, Grammar and Samāsa kernels.

Hierarchy
---------

DhatuContext
        │
        ▼
DhatuAnalysisCollection
        │
        ▼
DhatuResult

Future
------

Future versions may additionally expose

    • best_analysis

    • ambiguity_score

    • derivation_path

    • confidence_distribution

without changing the public API.

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.dhatu.dhatu_analysis import (
    DhatuAnalysis,
)

from SanskritAI.domain.dhatu.dhatu_analysis_collection import (
    DhatuAnalysisCollection,
)

from SanskritAI.domain.dhatu.dhatu_context import (
    DhatuContext,
)

from SanskritAI.domain.dhatu.dhatu_diagnostic import (
    DhatuDiagnostic,
)


@dataclass(frozen=True, slots=True)
class DhatuResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable result produced by the Dhatu Kernel.
    """

    context: DhatuContext

    analyses: DhatuAnalysisCollection = field(
        default_factory=DhatuAnalysisCollection
    )

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[
        DhatuDiagnostic,
        ...
    ] = field(default_factory=tuple)

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return self.context.identifier

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Dhatu Result"

    @property
    def display_text(self) -> str:

        state = (
            "Succeeded"
            if self.succeeded
            else "Failed"
        )

        return (
            f"{self.display_name}"
            f" [{state}]"
        )

    @property
    def display_description(self) -> str:

        if self.has_diagnostics:
            return self.diagnostics[0].message

        return ""

    # ---------------------------------------------------------
    # Context Convenience
    # ---------------------------------------------------------

    @property
    def subject(self):
        return self.context.subject

    @property
    def source(self) -> str:
        return self.context.source

    @property
    def language(self) -> str:
        return self.context.language

    @property
    def script(self) -> str:
        return self.context.script

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    @property
    def result(self) -> DhatuAnalysisCollection:
        return self.analyses

    @property
    def analysis_count(self) -> int:
        return self.analyses.count

    @property
    def has_analyses(self) -> bool:
        return not self.analyses.is_empty

    @property
    def first_analysis(
        self,
    ) -> DhatuAnalysis | None:
        return self.analyses.first

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def has_diagnostics(self) -> bool:
        return len(self.diagnostics) > 0

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def has_errors(self) -> bool:
        return any(
            diagnostic.is_error
            for diagnostic in self.diagnostics
        )

    @property
    def has_warnings(self) -> bool:
        return any(
            diagnostic.is_warning
            for diagnostic in self.diagnostics
        )

    @property
    def first_diagnostic(
        self,
    ) -> DhatuDiagnostic | None:

        if not self.diagnostics:
            return None

        return self.diagnostics[0]

    # ---------------------------------------------------------
    # Resolution State
    # ---------------------------------------------------------

    @property
    def resolved(self) -> bool:
        return (
            self.succeeded
            and self.has_analyses
        )

    @property
    def unresolved(self) -> bool:
        return not self.resolved

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    @property
    def best_analysis(
        self,
    ) -> DhatuAnalysis | None:
        """
        Currently returns the first analysis.

        Future versions may perform ranking.
        """
        return self.first_analysis

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
