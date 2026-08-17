
from __future__ import annotations

"""
SanskritAI
==========

Samāsa Resolution Kernel

Canonical orchestration layer for Samāsa resolution.

The generic kernel is intentionally repository-agnostic.

Responsibilities
----------------

• Accept a SamasaContext.
• Delegate analysis to the configured SamasaStrategy.
• Convert the domain-level SamasaResult into the canonical
  SamasaResolutionResult.
• Contain no Samāsa rules.
• Contain no repository logic.

Architecture
------------

SamasaContext
        │
        ▼
SamasaResolutionKernel
        │
        ▼
SamasaStrategy
        │
        ▼
DefaultSamasaStrategy
        │
        ▼
SamasaRuleSet
        │
        ▼
SamasaResult
        │
        ▼
SamasaResolutionResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.samasa.default_samasa_strategy import (
    DefaultSamasaStrategy,
)

from SanskritAI.domain.samasa.samasa_context import (
    SamasaContext,
)

from SanskritAI.domain.samasa.samasa_resolution_result import (
    SamasaResolutionResult,
)

from SanskritAI.domain.samasa.samasa_result import (
    SamasaResult,
)

from SanskritAI.domain.samasa.samasa_strategy import (
    SamasaStrategy,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SamasaResolutionKernel(
    Immutable,
    Displayable,
):
    """
    Canonical generic Samāsa Resolution Kernel.

    The kernel delegates linguistic analysis to the configured
    SamasaStrategy and converts the resulting SamasaResult into
    the canonical SamasaResolutionResult consumed by the
    resolution pipeline.
    """

    strategy: SamasaStrategy = field(
        default_factory=DefaultSamasaStrategy,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Samasa Resolution Kernel"

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
            "Canonical orchestration layer for the "
            "Samāsa Kernel."
        )

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    @property
    def resolution_strategy(
        self,
    ) -> SamasaStrategy:

        return self.strategy

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: SamasaContext,
    ) -> SamasaResolutionResult:
        """
        Executes Samāsa resolution.

        The configured strategy produces the domain-level
        SamasaResult. The kernel then promotes that result into
        the canonical SamasaResolutionResult used by the
        ResolutionPipeline.
        """

        result: SamasaResult = self.strategy.analyze(
            context,
        )

        return self._to_resolution_result(
            result,
        )

    # ---------------------------------------------------------
    # Result adaptation
    # ---------------------------------------------------------

    def _to_resolution_result(
        self,
        result: SamasaResult,
    ) -> SamasaResolutionResult:
        """
        Convert the domain-level SamasaResult into the
        canonical resolution-stage result.

        No new result model is introduced.
        """

        return SamasaResolutionResult(
            context=result.context,
            analyses=result.analyses,
            diagnostics=(),
            confidence=result.confidence,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __call__(
        self,
        context: SamasaContext,
    ) -> SamasaResolutionResult:

        return self.resolve(
            context,
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text
