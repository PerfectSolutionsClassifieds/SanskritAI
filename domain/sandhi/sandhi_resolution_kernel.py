
from __future__ import annotations

"""
SanskritAI
==========

Sandhi Resolution Kernel

Canonical orchestration layer for Sandhi resolution.

The kernel coordinates Sandhi resolution while delegating all
linguistic processing to the configured SandhiResolutionStrategy.

Responsibilities
----------------

• Accept a generic ResolutionContext.
• Adapt it to the domain-specific SandhiContext.
• Delegate resolution to the configured strategy.
• Return the canonical SandhiResult.

The kernel intentionally contains:

• no Sandhi rules
• no phonological rules
• no repository logic
• no rule-selection logic

Architecture
------------

ResolutionContext
        │
        ▼
SandhiContext
        │
        ▼
SandhiResolutionKernel
        │
        ▼
SandhiResolutionStrategy
        │
        ▼
DefaultSandhiStrategy
        │
        ▼
SandhiRuleSet
        │
        ▼
SandhiResult

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.sandhi.default_sandhi_strategy import (
    DefaultSandhiStrategy,
)

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)

from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)

from SanskritAI.domain.sandhi.sandhi_strategy import (
    SandhiStrategy,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SandhiResolutionKernel(
    Immutable,
    Displayable,
):
    """
    Canonical Sandhi Resolution Kernel.

    Acts as the public orchestration entry point for Sandhi
    resolution.

    The kernel does not implement Sandhi rules. It delegates
    linguistic resolution to the configured strategy.
    """

    strategy: SandhiStrategy = field(
        default_factory=DefaultSandhiStrategy,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Sandhi Resolution Kernel"

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
            "Sandhi Resolution Kernel."
        )

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    @property
    def resolution_strategy(
        self,
    ) -> SandhiStrategy:

        return self.strategy

    # ---------------------------------------------------------
    # Context Adaptation
    # ---------------------------------------------------------

    def build_context(
        self,
        context: ResolutionContext,
    ) -> SandhiContext:

        return SandhiContext(
            identifier=context.identifier,
            subject=context.subject,
            source=context.source,
            language=context.language,
            script=context.script,
            metadata=context.metadata,
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> SandhiResult:
        """
        Executes Sandhi resolution.

        The generic ResolutionContext is adapted to the
        Sandhi-specific context expected by the strategy.
        """

        sandhi_context = self.build_context(
            context,
        )

        return self.strategy.resolve(
            sandhi_context,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __call__(
        self,
        context: ResolutionContext,
    ) -> SandhiResult:

        return self.resolve(
            context,
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text
