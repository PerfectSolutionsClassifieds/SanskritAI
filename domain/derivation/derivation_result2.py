from __future__ import annotations

"""
SanskritAI
==========

Derivation Result

Defines the immutable outcome produced by every
Morphological Derivation operation.

Unlike the initial implementation, this version mirrors the
Dhatu, Pratyaya, Grammar and Samasa kernels by carrying a
DerivationAnalysisCollection instead of a generic value.

Version
-------
v1.1.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.derivation.derivation_analysis import (
    DerivationAnalysis,
)
from SanskritAI.domain.derivation.derivation_analysis_collection import (
    DerivationAnalysisCollection,
)
from SanskritAI.domain.derivation.derivation_context import (
    DerivationContext,
)
from SanskritAI.domain.derivation.derivation_diagnostic import (
    DerivationDiagnostic,
)


@dataclass(frozen=True, slots=True)
class DerivationResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable result produced by the Morphological
    Derivation Kernel.
    """

    context: DerivationContext

    analyses: DerivationAnalysisCollection = field(
        default_factory=DerivationAnalysisCollection
    )

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[
        DerivationDiagnostic,
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
        return "Derivation Result"

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
            return self.first_diagnostic.message

        if self.has_analyses:
            return (
                self.best_analysis.surface_form
            )

        return ""

    # ---------------------------------------------------------
    # Context shortcuts
    # ---------------------------------------------------------

    @property
    def subject(self):
        return self.context.subject

    @property
    def dhatu(self):
        return self.context.dhatu

    @property
    def pratyaya(self):
        return self.context.pratyaya

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
    # Analyses
    # ---------------------------------------------------------

    @property
    def has_analyses(self) -> bool:
        return not self.analyses.is_empty

    @property
    def analysis_count(self) -> int:
        return self.analyses.count

    @property
    def best_analysis(
        self,
    ) -> DerivationAnalysis | None:
        return self.analyses.first

    @property
    def result(
        self,
    ) -> DerivationAnalysis | None:
        """
        Convenience alias for the primary analysis.
        """
        return self.best_analysis

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    @property
    def has_diagnostics(self) -> bool:
        return bool(self.diagnostics)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def first_diagnostic(
        self,
    ) -> DerivationDiagnostic | None:

        if not self.diagnostics:
            return None

        return self.diagnostics[0]

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

    # ---------------------------------------------------------
    # Resolution
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

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
