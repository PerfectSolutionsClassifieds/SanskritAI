from __future__ import annotations

"""
SanskritAI
==========

Semantic Analysis Result

Thin compatibility wrapper over SemanticResult.

This module exists to provide a more analysis-oriented API
during the transition from a generic SemanticResult model to a
structured SemanticAnalysisCollection-oriented semantic kernel.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.semantic.semantic_analysis import SemanticAnalysis
from SanskritAI.domain.semantic.semantic_analysis_collection import (
    SemanticAnalysisCollection,
)
from SanskritAI.domain.semantic.semantic_context import SemanticContext
from SanskritAI.domain.semantic.semantic_diagnostic import (
    SemanticDiagnostic,
)
from SanskritAI.domain.semantic.semantic_result import SemanticResult


@dataclass(frozen=True, slots=True)
class SemanticAnalysisResult(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Thin compatibility wrapper that presents a semantic result
    through analysis-oriented terminology.
    """

    context: SemanticContext

    analyses: SemanticAnalysisCollection = field(
        default_factory=SemanticAnalysisCollection
    )

    succeeded: bool = True

    confidence: float = 1.0

    diagnostics: tuple[
        SemanticDiagnostic,
        ...
    ] = field(default_factory=tuple)

    @classmethod
    def from_result(
        cls,
        result: SemanticResult,
    ) -> "SemanticAnalysisResult":
        """
        Builds a compatibility wrapper from a SemanticResult.
        """
        value = result.value

        if isinstance(value, SemanticAnalysisCollection):
            analyses = value
        elif value is None:
            analyses = SemanticAnalysisCollection()
        else:
            analyses = SemanticAnalysisCollection(
                analyses=(
                    SemanticAnalysis(
                        identifier=f"{result.identifier}:analysis:1",
                        text=str(result.subject),
                        meaning=str(value),
                        semantic_type="Semantic",
                        confidence=result.confidence,
                        matched_rule="SemanticResult",
                        notes="Wrapped from generic SemanticResult value.",
                    ),
                )
            )

        return cls(
            context=result.context,
            analyses=analyses,
            succeeded=result.succeeded,
            confidence=result.confidence,
            diagnostics=result.diagnostics,
        )

    @property
    def identifier(self) -> str:
        return self.context.identifier

    @property
    def display_name(self) -> str:
        return "Semantic Analysis Result"

    @property
    def display_text(self) -> str:
        state = "Succeeded" if self.succeeded else "Failed"
        return f"{self.display_name} [{state}]"

    @property
    def display_description(self) -> str:
        if self.has_diagnostics:
            return self.diagnostics[0].message
        if self.has_analyses:
            return self.first_analysis.display_text
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
    def has_analyses(self) -> bool:
        return not self.analyses.is_empty

    @property
    def analysis_count(self) -> int:
        return self.analyses.count

    @property
    def first_analysis(self) -> SemanticAnalysis | None:
        return self.analyses.first

    @property
    def result(self) -> SemanticAnalysisCollection:
        return self.analyses

    @property
    def has_diagnostics(self) -> bool:
        return bool(self.diagnostics)

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def first_diagnostic(self) -> SemanticDiagnostic | None:
        if not self.diagnostics:
            return None
        return self.diagnostics[0]

    @property
    def resolved(self) -> bool:
        return self.succeeded and self.has_analyses

    @property
    def unresolved(self) -> bool:
        return not self.resolved

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    def to_result(self) -> SemanticResult:
        """
        Converts the wrapper back into the canonical SemanticResult.
        """
        return SemanticResult(
            context=self.context,
            value=self.analyses,
            succeeded=self.succeeded,
            confidence=self.confidence,
            diagnostics=self.diagnostics,
        )

    def __str__(self) -> str:
        return self.display_text
