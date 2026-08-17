
from __future__ import annotations

"""
SanskritAI
==========

Default Samāsa Resolution Kernel

Provides the canonical concrete Samāsa Resolution Kernel used
by SamasaService.

Architecture
------------

SamasaService
        │
        ▼
DefaultSamasaResolutionKernel
        │
        ▼
SamasaResolutionKernel
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

Notes
-----

The generic SamasaResolutionKernel is repository-agnostic.

The repository is retained explicitly by this concrete
composition object so that repository ownership remains at the
service/domain boundary.

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

from SanskritAI.domain.samasa.default_samasa_strategy import (
    DefaultSamasaStrategy,
)

from SanskritAI.domain.samasa.samasa_repository import (
    SamasaRepository,
)

from SanskritAI.domain.samasa.samasa_resolution_kernel import (
    SamasaResolutionKernel,
)

from SanskritAI.domain.samasa.samasa_resolution_result import (
    SamasaResolutionResult,
)

from SanskritAI.domain.samasa.samasa_strategy import (
    SamasaStrategy,
)

from SanskritAI.domain.samasa.samasa_context import (
    SamasaContext,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultSamasaResolutionKernel(
    Immutable,
    Displayable,
):
    """
    Canonical concrete Samāsa Resolution Kernel.

    This class is intentionally thin.

    It owns the repository composition boundary and delegates
    actual resolution to SamasaResolutionKernel.
    """

    repository: SamasaRepository

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

        return "Default Samasa Resolution Kernel"

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
            "Default concrete Samāsa Resolution Kernel "
            "composed with a canonical SamasaRepository."
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
    # Generic Kernel
    # ---------------------------------------------------------

    @property
    def kernel(
        self,
    ) -> SamasaResolutionKernel:

        return SamasaResolutionKernel(
            strategy=self.strategy,
        )

    # ---------------------------------------------------------
    # Context Adaptation
    # ---------------------------------------------------------

    def build_context(
        self,
        context: ResolutionContext,
    ) -> SamasaContext:
        """
        Adapt the application-level ResolutionContext into the
        Samāsa-specific context.

        Additional Samāsa-specific controls are preserved through
        metadata when supplied by the upstream resolution layer.
        """

        return SamasaContext(
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
    ) -> SamasaResolutionResult:
        """
        Resolve the supplied application-level context.

        The concrete kernel adapts the context and delegates the
        actual resolution to the repository-agnostic kernel.
        """

        samasa_context = self.build_context(
            context,
        )

        return self.kernel.resolve(
            samasa_context,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __call__(
        self,
        context: ResolutionContext,
    ) -> SamasaResolutionResult:

        return self.resolve(
            context,
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text
