from __future__ import annotations

"""
SanskritAI
==========

Sandhi Resolver

Defines the façade for Sandhi resolution.

SandhiResolver mirrors the architecture established by the
Resolution, Morphology, Grammar, and Lexical kernels.

The resolver itself performs no linguistic processing. It
delegates all Sandhi computation to a configured
SandhiStrategy.

Hierarchy
---------

SandhiResolver
        │
        └── DefaultSandhiResolver

Version
-------
v1.0.0
"""

from SanskritAI.core.mixins.displayable import (
    Displayable,
)

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)

from SanskritAI.domain.sandhi.sandhi_result import (
    SandhiResult,
)

from SanskritAI.domain.sandhi.sandhi_strategy import (
    SandhiStrategy,
)


class SandhiResolver(
    Displayable,
):
    """
    Canonical façade for Sandhi resolution.
    """

    def __init__(
        self,
        strategy: SandhiStrategy,
    ) -> None:

        self._strategy = strategy

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

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
            "Delegates Sandhi resolution to a strategy."
        )

    # ---------------------------------------------------------
    # Strategy
    # ---------------------------------------------------------

    @property
    def strategy(
        self,
    ) -> SandhiStrategy:
        """
        Configured Sandhi strategy.
        """
        return self._strategy

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: SandhiContext,
    ) -> SandhiResult:
        """
        Delegates Sandhi resolution.
        """

        return self.strategy.resolve(
            context,
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
