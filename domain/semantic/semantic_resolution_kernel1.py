from __future__ import annotations

"""
SanskritAI
==========

Semantic Resolution Kernel

Canonical orchestration layer for Semantic resolution.

Responsibilities
----------------
• Accept a SemanticContext.
• Delegate semantic analysis to SemanticStrategy.
• Convert SemanticResult into SemanticResolutionResult.
• Convert domain SemanticDiagnostic objects into the
  repository-wide ResolutionDiagnostic objects.
• Remain independent of SemanticRepository.

Architecture
------------

SemanticContext
        │
        ▼
SemanticResolutionKernel
        │
        ▼
SemanticStrategy
        │
        ▼
DefaultSemanticStrategy
        │
        ▼
SemanticResult
        │
        ▼
SemanticResolutionResult
        │
        ▼
ResolutionResult

No additional result model is introduced.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.semantic.semantic_context import (
    SemanticContext,
)

from SanskritAI.domain.semantic.semantic_result import (
    SemanticResult,
)

from SanskritAI.domain.semantic.semantic_resolution_result import (
    SemanticResolutionResult,
)

from SanskritAI.domain.semantic.semantic_strategy import (
    SemanticStrategy,
)

from SanskritAI.domain.semantic.default_semantic_strategy import (
    DefaultSemanticStrategy,
)

from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
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

    The kernel owns orchestration only.

    Linguistic interpretation remains the responsibility of the
    configured SemanticStrategy.
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
        Execute semantic analysis.

        The strategy produces the domain-level SemanticResult.
        The kernel promotes that result into the canonical
        SemanticResolutionResult consumed by the Resolution
        Pipeline.
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
        Convert SemanticResult into the canonical
        SemanticResolutionResult.

        Existing SemanticResult and SemanticResolutionResult
        models are deliberately reused.

        No duplicate result model is introduced.
        """

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

        value = result.value

        if value is None:
            from SanskritAI.domain.semantic.semantic_analysis_collection import (
                SemanticAnalysisCollection,
            )

            analyses = SemanticAnalysisCollection()
        else:
            analyses = value

        return SemanticResolutionResult(
            context=context_from_result(result),
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


def context_from_result(
    result: SemanticResult,
) -> object:
    """
    Return the original SemanticContext carried by the
    SemanticResult.

    Kept as a small function to make the result adaptation
    explicit without introducing another abstraction.
    """

    return result.context
