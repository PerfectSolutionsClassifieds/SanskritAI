from __future__ import annotations

"""
SanskritAI
==========

Resolution Strategy

Defines the abstract strategy responsible for resolving a
ResolutionContext into a ResolutionResult.

ResolutionStrategy represents the algorithm used by a resolver.

Concrete domain kernels implement their own strategies, for
example:

    • LexicalResolutionStrategy

    • MorphologicalResolutionStrategy

    • SandhiResolutionStrategy

    • SamāsaResolutionStrategy

    • DhātuResolutionStrategy

    • GrammarResolutionStrategy

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


class ResolutionStrategy(
    ABC,
    Displayable,
):
    """
    Abstract resolution strategy.

    A strategy encapsulates the algorithm used to resolve a
    domain object.
    """

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
            "Abstract domain resolution strategy."
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    @abstractmethod
    def resolve(
        self,
        context: ResolutionContext,
    ) -> ResolutionResult:
        """
        Resolves the supplied context.

        Parameters
        ----------
        context:
            Resolution context.

        Returns
        -------
        ResolutionResult
        """
        raise NotImplementedError
