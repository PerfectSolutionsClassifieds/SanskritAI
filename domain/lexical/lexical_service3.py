from __future__ import annotations

"""
SanskritAI
==========

Lexical Service

Abstract application-facing lexical resolution service.

Responsibilities
----------------

• coordinates lexical resolution

• enriches ResolutionState

• delegates lookup to LexicalLookupEngine

This abstraction intentionally contains no repository logic.

Architecture
------------

ResolutionPipeline
        │
        ▼
LexicalResolutionStage
        │
        ▼
LexicalService
        │
        ▼
DefaultLexicalService
        │
        ▼
LexicalLookupEngine
        │
        ▼
LexicalRepository
        │
        ▼
CanonicalKnowledgeRepository

Version
-------
v3.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.resolution.resolution_state import (
    ResolutionState,
)


class LexicalService(
    ABC,
    Displayable,
):
    """
    Abstract lexical resolution service.
    """

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
            "Abstract lexical resolution service."
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    @abstractmethod
    def resolve(
        self,
        state: ResolutionState,
    ) -> ResolutionState:
        """
        Performs lexical resolution.

        Implementations enrich the supplied ResolutionState
        with a LexicalResolutionResult.

        Parameters
        ----------
        state

            Current pipeline resolution state.

        Returns
        -------
        ResolutionState

            Enriched pipeline state.
        """
        raise NotImplementedError

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.display_text
