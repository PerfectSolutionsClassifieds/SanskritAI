from __future__ import annotations

"""
SanskritAI
==========

Morphological Resolution Strategy

Defines the strategy abstraction responsible for resolving
morphological information for a lexical resolution.

The strategy itself performs no grammatical analysis.
Instead it orchestrates one or more MorphologicalAnalyzer
implementations and converts their output into a canonical
MorphologicalResolutionResult.

Architecture
------------

LexicalResolutionResult
        │
        ▼
MorphologicalResolutionStrategy
        │
        ▼
MorphologicalAnalyzer
        │
        ▼
MorphologicalAnalysisCollection
        │
        ▼
MorphologicalResolutionResult

Version
-------
v2.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.morphology.morphological_resolution_context import (
    MorphologicalResolutionContext,
)

from SanskritAI.domain.morphology.morphological_resolution_result import (
    MorphologicalResolutionResult,
)


class MorphologicalResolutionStrategy(
    ABC,
    Displayable,
):
    """
    Strategy interface for morphological resolution.
    """

    @property
    def display_name(
        self,
    ) -> str:
        return self.__class__.__name__

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
            "Strategy responsible for orchestrating "
            "morphological analysis."
        )

    @abstractmethod
    def resolve(
        self,
        context: MorphologicalResolutionContext,
    ) -> MorphologicalResolutionResult:
        """
        Performs morphological resolution.

        Parameters
        ----------
        context
            Morphological resolution context.

        Returns
        -------
        MorphologicalResolutionResult
        """
        raise NotImplementedError
