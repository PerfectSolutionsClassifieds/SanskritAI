from __future__ import annotations

"""
SanskritAI
==========

Resolution Contributor

Defines the contract implemented by every linguistic
resolution service.

Purpose
-------

A ResolutionContributor performs one linguistic analysis
and returns an enriched ResolutionResult.

This removes all stage-specific branching from the
ResolutionPipeline.

Pipeline

ResolutionResult
        │
        ▼
ResolutionContributor
        │
        ▼
ResolutionResult

Every contributor enriches the existing immutable aggregate
rather than constructing an entirely new pipeline object.

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)

from SanskritAI.domain.resolution.resolution_result import (
    ResolutionResult,
)


class ResolutionContributor(
    ABC,
    Displayable,
):
    """
    Contract implemented by every linguistic service.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Contributes one linguistic resolution stage "
            "to the aggregate ResolutionResult."
        )

    @abstractmethod
    def contribute(
        self,
        aggregate: ResolutionResult,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Performs one linguistic analysis and returns an
        enriched ResolutionResult.

        Parameters
        ----------
        aggregate

            Current aggregate ResolutionResult.

        context

            Immutable ResolutionContext.

        Returns
        -------
        ResolutionResult

            Updated immutable aggregate.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text
