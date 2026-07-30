from __future__ import annotations

"""
SanskritAI
==========

Lexical Resolver

Public façade of the Lexical Resolution subsystem.

A LexicalResolver delegates lexical resolution to a configured
LexicalResolutionStrategy.

Relationship
------------

ResolutionContext
        │
        ▼
LexicalResolver
        │
        ▼
LexicalResolutionStrategy
        │
        ▼
LexicalResolutionResult

Version
-------
v1.0.0
"""

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.lexical.lexical_resolution_strategy import (
    LexicalResolutionStrategy,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolver import (
    Resolver,
)


class LexicalResolver(
    Resolver,
):
    """
    Public lexical resolver.

    Delegates lexical resolution to the configured
    LexicalResolutionStrategy.
    """

    def __init__(
        self,
        strategy: LexicalResolutionStrategy,
    ) -> None:

        super().__init__(
            strategy=strategy,
        )

    # ---------------------------------------------------------
    # Typed Strategy
    # ---------------------------------------------------------

    @property
    def strategy(
        self,
    ) -> LexicalResolutionStrategy:
        return super().strategy

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> LexicalResolutionResult:
        """
        Resolves lexical information.
        """

        return self.strategy.resolve(
            context,
        )

    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Lexical Resolver"

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Facade over lexical resolution strategies."
        )
