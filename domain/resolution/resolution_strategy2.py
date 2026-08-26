
from __future__ import annotations

"""
SanskritAI
==========

Resolution Strategy

Defines the abstract strategy contract used by the
resolution framework.

A ResolutionStrategy encapsulates the algorithm used to
resolve a ResolutionContext into a ResolutionResult.

Strategies are intentionally stateless and reusable.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


class ResolutionStrategy(
    ABC,
    Displayable,
):
    """
    Abstract resolution strategy.

    A strategy receives a ResolutionContext and produces
    a ResolutionResult.

    Implementations should remain stateless so that the
    same strategy instance can safely be reused.
    """

    __slots__ = ()

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Strategy for resolving a linguistic "
            "ResolutionContext."
        )

    @abstractmethod
    def resolve(
        self,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Resolve the supplied context.

        Parameters
        ----------
        context:
            Resolution context to resolve.

        Returns
        -------
        ResolutionResult
            Result produced by this strategy.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text
