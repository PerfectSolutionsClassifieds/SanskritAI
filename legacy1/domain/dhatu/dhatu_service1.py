from __future__ import annotations

"""
SanskritAI
==========

Dhatu Service

Application-facing façade for the Dhātu Kernel.

The DhatuService provides the stable service boundary between
higher-level SanskritAI components and the Dhātu domain kernel.

Responsibilities
----------------
• Accept canonical DhatuContext objects.
• Delegate Dhātu analysis to the configured DhatuResolver.
• Expose the resulting DhatuResult.
• Keep higher-level components independent of the concrete
  Dhātu strategy implementation.

Architecture
------------

KnowledgeServiceRegistry
        │
        ▼
DhatuService
        │
        ▼
DhatuResolver
        │
        ▼
DhatuStrategy
        │
        ▼
DhatuResult

The service intentionally contains no Dhātu business rules.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.dhatu.dhatu_context import (
    DhatuContext,
)

from SanskritAI.domain.dhatu.dhatu_resolver import (
    DhatuResolver,
)

from SanskritAI.domain.dhatu.dhatu_result import (
    DhatuResult,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DhatuService(
    Displayable,
):
    """
    Application-facing façade over the Dhātu Kernel.
    """

    resolver: DhatuResolver

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Dhatu Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Application-facing façade for canonical "
            "Dhātu analysis."
        )

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    def analyze(
        self,
        context: DhatuContext,
    ) -> DhatuResult:
        """
        Analyze the supplied Dhātu context.

        All domain analysis remains delegated to the
        configured DhatuResolver.
        """

        return self.resolver.analyze(
            context,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def resolve(
        self,
        context: DhatuContext,
    ) -> DhatuResult:
        """
        Alias for analyze().

        This provides a terminology-neutral service boundary
        for callers that use 'resolve' for linguistic
        resolution operations.
        """

        return self.analyze(
            context,
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
