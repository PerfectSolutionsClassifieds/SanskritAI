from __future__ import annotations

"""
SanskritAI
==========

Default Morphological Resolution Kernel

Provides the canonical concrete Morphological Resolution Kernel
used by MorphologicalService.

Architecture
------------

MorphologicalService
        │
        ▼
DefaultMorphologicalResolutionKernel
        │
        ▼
MorphologicalResolutionKernel
        │
        ▼
DefaultMorphologicalResolutionStrategy
        │
        ▼
DefaultMorphologicalAnalyzer
        │
        ▼
MorphologicalRuleSet

Notes
-----

The generic MorphologicalResolutionKernel is intentionally
repository-agnostic.

This concrete kernel exists at the domain-service boundary so
that MorphologicalService can compose a repository with the
resolution kernel without placing repository logic inside the
generic kernel.

The repository is therefore retained as an explicit dependency
of this concrete composition object.

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.morphology.default_morphological_resolution_strategy import (
    DefaultMorphologicalResolutionStrategy,
)

from SanskritAI.domain.morphology.morphological_repository import (
    MorphologicalRepository,
)

from SanskritAI.domain.morphology.morphological_resolution_context import (
    MorphologicalResolutionContext,
)

from SanskritAI.domain.morphology.morphological_resolution_kernel import (
    MorphologicalResolutionKernel,
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
class DefaultMorphologicalResolutionKernel(
    Immutable,
    Displayable,
):
    """
    Canonical concrete Morphology Resolution Kernel.

    This class is a thin composition layer over the generic
    MorphologicalResolutionKernel.

    Repository ownership remains explicit here so the service
    layer can construct the kernel with its canonical repository.
    """

    repository: MorphologicalRepository

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
        return "Default Morphological Resolution Kernel"

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
            "Default concrete Morphology Resolution Kernel "
            "composed with a canonical MorphologicalRepository."
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
    # Generic Kernel
    # ---------------------------------------------------------

    @property
    def kernel(
        self,
    ) -> MorphologicalResolutionKernel:
        """
        Creates the repository-agnostic resolution kernel.

        Repository access is intentionally not pushed into the
        generic kernel.
        """
        return MorphologicalResolutionKernel(
            strategy=self.strategy,
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: MorphologicalResolutionContext,
    ) -> MorphologicalResolutionResult:
        """
        Resolves the supplied morphology context.

        The repository is retained as part of the concrete
        composition boundary. The current rule-based analyzer
        does not yet consume repository data directly.
        """

        return self.kernel.resolve(
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
