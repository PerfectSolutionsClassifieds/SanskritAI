
from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Resolution Kernel

Provides the canonical concrete Sandhi Resolution Kernel used
by SandhiService.

Architecture
------------

SandhiService
        │
        ▼
DefaultSandhiResolutionKernel
        │
        ▼
SandhiResolutionKernel
        │
        ▼
DefaultSandhiStrategy
        │
        ▼
SandhiRuleSet
        │
        ▼
SandhiResult

Notes
-----

The repository is retained as an explicit dependency of the
concrete composition boundary.

The generic SandhiResolutionKernel remains repository-agnostic.

The concrete kernel does not implement Sandhi rules. All
linguistic processing remains delegated to the configured
SandhiResolutionStrategy.

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

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.sandhi.sandhi_resolution_kernel import (
    SandhiResolutionKernel,
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
class DefaultSandhiResolutionKernel(
    Immutable,
    Displayable,
):
    """
    Canonical concrete Sandhi Resolution Kernel.

    This is a thin composition layer over the generic
    SandhiResolutionKernel.

    Repository ownership remains explicit here so the service
    layer can construct the kernel with its canonical repository.
    """

    repository: SandhiRepository

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

        return "Default Sandhi Resolution Kernel"

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
            "Default concrete Sandhi Resolution Kernel "
            "composed with a canonical SandhiRepository."
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
    # Generic Kernel
    # ---------------------------------------------------------

    @property
    def kernel(
        self,
    ) -> SandhiResolutionKernel:
        """
        Creates the repository-agnostic Sandhi resolution kernel.

        Repository access remains at this concrete composition
        boundary.
        """

        return SandhiResolutionKernel(
            strategy=self.strategy,
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> SandhiResult:
        """
        Resolves the supplied generic ResolutionContext.

        The repository remains part of the concrete composition
        boundary. The current rule-based Sandhi strategy operates
        through its configured SandhiRuleSet.
        """

        return self.kernel.resolve(
            context,
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
