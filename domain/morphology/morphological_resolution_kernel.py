from __future__ import annotations

"""
SanskritAI
==========

Morphological Resolution Kernel

Purpose
-------
Canonical orchestration layer for the Morphology Kernel.

The kernel coordinates the complete morphology pipeline while
delegating linguistic work to the configured resolution
strategy.

Responsibilities
----------------

• Accept MorphologicalResolutionContext

• Delegate resolution to the configured
  MorphologicalResolutionStrategy

• Return a canonical MorphologicalResolutionResult

The kernel intentionally contains no grammatical rules and no
repository logic.

Architecture
------------

MorphologicalResolutionContext
            │
            ▼
MorphologicalResolutionKernel
            │
            ▼
MorphologicalResolutionStrategy
            │
            ▼
DefaultMorphologicalResolutionStrategy
            │
            ▼
MorphologicalAnalyzer
            │
            ▼
MorphologicalRuleSet
            │
            ▼
MorphologicalResolutionResult

Version
-------
v2.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.morphology.default_morphological_resolution_strategy import (
    DefaultMorphologicalResolutionStrategy,
)

from SanskritAI.domain.morphology.morphological_resolution_context import (
    MorphologicalResolutionContext,
)

from SanskritAI.domain.morphology.morphological_resolution_result import (
    MorphologicalResolutionResult,
)

from SanskritAI.domain.morphology.morphological_resolution_strategy import (
    MorphologicalResolutionStrategy,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MorphologicalResolutionKernel(
    Immutable,
    Displayable,
):
    """
    Canonical Morphology Kernel.

    Acts as the public entry point for all morphology
    resolution.
    """

    strategy: MorphologicalResolutionStrategy = field(
        default_factory=DefaultMorphologicalResolutionStrategy,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Morphological Resolution Kernel"

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
            "Morphology Kernel."
        )

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    @property
    def resolution_strategy(
        self,
    ) -> MorphologicalResolutionStrategy:

        return self.strategy

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: MorphologicalResolutionContext,
    ) -> MorphologicalResolutionResult:
        """
        Executes the complete morphology pipeline.

        Parameters
        ----------
        context
            Morphological execution context.

        Returns
        -------
        MorphologicalResolutionResult
        """

        return self.strategy.resolve(
            context,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __call__(
        self,
        context: MorphologicalResolutionContext,
    ) -> MorphologicalResolutionResult:

        return self.resolve(
            context,
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text
