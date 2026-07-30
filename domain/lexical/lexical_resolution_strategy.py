from __future__ import annotations

"""
SanskritAI
==========

Lexical Resolution Strategy

Defines the abstract strategy responsible for resolving
lexical information.

A LexicalResolutionStrategy specializes the generic
ResolutionStrategy for the Lexical Kernel.

Concrete implementations include:

    • DefaultLexicalResolutionStrategy
    • MorphologyAwareLexicalResolutionStrategy
    • SandhiAwareLexicalResolutionStrategy
    • SamasaAwareLexicalResolutionStrategy
    • SemanticLexicalResolutionStrategy

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)
from SanskritAI.domain.resolution.resolution_strategy import (
    ResolutionStrategy,
)
from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)


class LexicalResolutionStrategy(
    ResolutionStrategy,
    ABC,
):
    """
    Abstract lexical resolution strategy.
    """

    @abstractmethod
    def resolve(
        self,
        context: ResolutionContext,
    ) -> LexicalResolutionResult:
        """
        Resolves lexical information for the supplied context.
        """
        raise NotImplementedError
