from __future__ import annotations

"""
SanskritAI
==========

Semantic Resolution Kernel

Canonical orchestration layer for Semantic resolution.

The kernel delegates linguistic analysis to SemanticStrategy
and promotes the resulting SemanticResult into the existing
SemanticResolutionResult used by the Resolution Pipeline.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)

from SanskritAI.domain.semantic.default_semantic_strategy import (
    DefaultSemanticStrategy,
)

from SanskritAI.domain.semantic.semantic_context import (
    SemanticContext,
)

from SanskritAI.domain.semantic.semantic_resolution_result import (
    SemanticResolutionResult,
)

from SanskritAI.domain.semantic.semantic_result import (
    SemanticResult,
)

from SanskritAI.domain.semantic.semantic_strategy import (
    SemanticStrategy,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SemanticResolutionKernel(
    Immutable,
    Displayable,
):
    """
    Repository-agnostic Semantic Resolution Kernel.

    Responsibilities
    ----------------
    • Orchestrate semantic resolution.
    • Delegate analysis to SemanticStrategy.
    • Adapt SemanticResult into SemanticResolutionResult.
    • Adapt SemanticDiagnostic into ResolutionDiagnostic.

    The kernel contains no repository logic and no semantic
    linguistic rules.
    """

    strategy: SemanticStrategy = field(
        default_factory=DefaultSemanticStrategy,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Semantic Resolution Kernel"

    @property
    def display_text(
        self,
    ) -> str:

        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:

        return (
            "Canonical orchestration layer for Semantic "
            "resolution."
        )

    # ---------------------------------------------------------
    # Strategy
    # ---------------------------------------------------------

    @property
    def resolution_strategy(
        self,
    ) -> SemanticStrategy:

        return self.strategy

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: SemanticContext,
    ) -> SemanticResolutionResult:
        """
        Execute Semantic resolution.
        """

        result = self.strategy.analyze(
            context,
        )

        return self._to_resolution_result(
            result,
        )

    # ---------------------------------------------------------
    # Result adaptation
    # ---------------------------------------------------------

    @staticmethod
    def _to_resolution_result(
        result: SemanticResult,
    ) -> SemanticResolutionResult:
        """
        Promote the domain SemanticResult into the canonical
        SemanticResolutionResult.

        Existing result models are reused. No duplicate result
        model is introduced.
        """

        from SanskritAI.domain.semantic.semantic_analysis_collection import (
            SemanticAnalysisCollection,
        )

        value = result.value

        if isinstance(
            value,
            SemanticAnalysisCollection,
        ):
            analyses = value
        else:
            analyses = SemanticAnalysisCollection()

        diagnostics = tuple(
            ResolutionDiagnostic(
                code=diagnostic.code,
                message=diagnostic.message,
                severity=diagnostic.severity,
                source=(
                    getattr(
                        diagnostic,
                        "rule",
                        "",
                    )
                    or "SemanticKernel"
                ),
                recoverable=(
                    diagnostic.severity.upper()
                    != "ERROR"
                ),
            )
            for diagnostic in result.diagnostics
        )

        return SemanticResolutionResult(
            context=result.context,
            analyses=analyses,
            diagnostics=diagnostics,
            confidence=result.confidence,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __call__(
        self,
        context: SemanticContext,
    ) -> SemanticResolutionResult:

        return self.resolve(
            context,
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text
