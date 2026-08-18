from __future__ import annotations

"""
SanskritAI
==========

Default Dhatu Service

Canonical default implementation of DhatuService.

Architecture
------------

KnowledgeServiceRegistry
        │
        ▼
DefaultDhatuService
        │
        ▼
DhatuResolver
        │
        ▼
DefaultDhatuResolver
        │
        ▼
DefaultDhatuStrategy
        │
        ▼
DhatuRuleSet
        │
        ▼
DhatuResult

Design
------

The service is intentionally thin.

It does not:

    • implement Dhatu rules
    • access the repository directly
    • construct the KnowledgeServiceRegistry
    • depend on CanonicalKnowledgeRepository

All Dhatu analysis remains delegated to the configured
DhatuResolver.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.dhatu.default_dhatu_resolver import (
    DefaultDhatuResolver,
)
from SanskritAI.domain.dhatu.dhatu_context import DhatuContext
from SanskritAI.domain.dhatu.dhatu_resolver import DhatuResolver
from SanskritAI.domain.dhatu.dhatu_result import DhatuResult
from SanskritAI.domain.dhatu.dhatu_service import DhatuService


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultDhatuService(
    DhatuService,
):
    """
    Canonical default Dhatu service.

    The default resolver is created lazily by the dataclass
    field factory and may be replaced through dependency
    injection for testing or future strategy implementations.
    """

    resolver: DhatuResolver = field(
        default_factory=DefaultDhatuResolver,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Default Dhatu Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical application service over the "
            "Dhatu resolution kernel."
        )

    # ---------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------

    def analyze(
        self,
        context: DhatuContext,
    ) -> DhatuResult:
        """
        Analyze the supplied Dhatu context.

        Delegation remains entirely within DhatuService.
        This override exists only to provide the concrete
        service boundary and an explicit public API.
        """

        return self.resolver.analyze(
            context,
        )

    # ---------------------------------------------------------
    # Resolution Alias
    # ---------------------------------------------------------

    def resolve(
        self,
        context: DhatuContext,
    ) -> DhatuResult:
        """
        Terminology-neutral alias for analyze().
        """

        return self.analyze(
            context,
        )

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
