
from __future__ import annotations

"""
SanskritAI
==========

Resolver

Coordinates execution of a ResolutionStrategy.

The Resolver is intentionally thin. It owns a single
immutable strategy dependency and delegates resolution
to that strategy.

Version
-------
v1.0.0
"""

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)

from SanskritAI.domain.resolution.resolution_strategy import (
    ResolutionStrategy,
)


class Resolver:
    """
    Executes a ResolutionStrategy.

    The strategy is supplied once during construction and
    is read-only thereafter.
    """

    __slots__ = (
        "_strategy",
        "_initialized",
    )

    def __init__(
        self,
        strategy: ResolutionStrategy,
    ) -> None:

        object.__setattr__(
            self,
            "_strategy",
            strategy,
        )

        object.__setattr__(
            self,
            "_initialized",
            True,
        )

    @property
    def strategy(self) -> ResolutionStrategy:
        """
        Return the configured resolution strategy.
        """
        return self._strategy

    def resolve(
        self,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Delegate resolution to the configured strategy.
        """
        return self._strategy.resolve(
            context,
        )

    def __setattr__(
        self,
        name: str,
        value: object,
    ) -> None:
        """
        Prevent mutation after initialization.

        Resolver dependencies are architectural configuration,
        not runtime state.
        """

        if getattr(
            self,
            "_initialized",
            False,
        ):
            raise AttributeError(
                "Resolver is immutable."
            )

        object.__setattr__(
            self,
            name,
            value,
        )
