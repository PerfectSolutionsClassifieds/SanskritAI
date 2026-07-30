from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Result

Defines the immutable outcome produced by every Pratyaya
analysis.

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.pratyaya.pratyaya_analysis import (
    PratyayaAnalysis,
)
from SanskritAI.domain.pratyaya.pratyaya_analysis_collection import (
    PratyayaAnalysisCollection,
)
from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext
from SanskritAI.domain.pratyaya.pratyaya_diagnostic import (
    PratyayaDiagnostic,
)


@dataclass(frozen=True, slots=True)
class PratyayaResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable result produced by the Pratyaya Kernel.
    """

    context: PratyayaContext

    analyses: PratyayaAnalysisCollection = field(
        default_factory=PratyayaAnalysisCollection
    )

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[
        PratyayaDiagnostic,
        ...
    ] = field(default_factory=tuple)

    @property
    def identifier(self) -> str:
        return self.context.identifier

    @property
    def display_name(self) -> str:
        return "Pratyaya Result"

    @property
    def display_text(self) -> str:
        state = "Succeeded" if self.succeeded else "Failed"
        return f"{self.display_name} [{state}]"

    @property
    def display_description(self) -> str:
        if self.has_diagnostics:
            return self.diagnostics[0].message
        return ""

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

    @property
    def result(self) -> PratyayaAnalysisCollection:
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
    ) -> PratyayaAnalysis | None:
        return self.analyses.first

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
    ) -> PratyayaDiagnostic | None:
        if not self.diagnostics:
            return None
        return self.diagnostics[0]

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
    ) -> PratyayaAnalysis | None:
        return self.first_analysis

    def __str__(self) -> str:
        return self.display_text
