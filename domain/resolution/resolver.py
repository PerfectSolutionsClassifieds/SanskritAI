from __future__ import annotations

"""
SanskritAI
==========

Resolver

Defines the abstract façade over a ResolutionStrategy.

Resolvers represent the public entry point into a resolution
kernel, while strategies encapsulate the underlying resolution
algorithm.

Relationship
------------

ResolutionContext
        │
        ▼
Resolver
        │
        ▼
ResolutionStrategy
        │
        ▼
ResolutionResult

Version
-------
v1.0.0
"""

from abc import ABC

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_strategy import (
    ResolutionStrategy,
)


class Resolver(
    ABC,
    Displayable,
):
    """
    Abstract domain resolver.

    Delegates the actual resolution work to a ResolutionStrategy.
    """

    def __init__(
        self,
        strategy: ResolutionStrategy,
    ) -> None:

        self._strategy = strategy

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Abstract domain resolver."
        )

    # ---------------------------------------------------------
    # Strategy
    # ---------------------------------------------------------

    @property
    def strategy(
        self,
    ) -> ResolutionStrategy:
        """
        Resolution strategy.
        """
        return self._strategy

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Resolves the supplied context by delegating to the
        configured strategy.
        """

        return self.strategy.resolve(context)

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
