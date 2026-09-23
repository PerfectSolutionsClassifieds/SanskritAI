from __future__ import annotations

"""
SanskritAI
==========

Resolution Stage

Defines the canonical interface for every stage of the
SanskritAI Resolution Pipeline.

A ResolutionStage performs one logical enrichment of an
existing ResolutionContext.

The stage never owns linguistic knowledge.

Instead, it delegates to the appropriate domain service
(LexicalService, MorphologicalService, SandhiService,
SamasaService, SemanticService, etc.) and returns a new,
enriched ResolutionContext.

Pipeline
--------

ResolutionContext
        │
        ▼
ResolutionStage
        │
        ▼
ResolutionContext

Future stages
-------------

• LexicalResolutionStage

• MorphologyResolutionStage

• SandhiResolutionStage

• SamasaResolutionStage

• SemanticResolutionStage

• PragmaticsResolutionStage

• CommentaryResolutionStage

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


class ResolutionStage(
    ABC,
    Displayable,
):
    """
    Abstract Resolution Pipeline stage.

    Each stage enriches an existing ResolutionContext and
    returns a new ResolutionContext.
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
            "Abstract resolution pipeline stage."
        )

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:
        return self.__class__.__name__

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    @abstractmethod
    def execute(
        self,
        context: ResolutionContext,
    ) -> ResolutionContext:
        """
        Executes this stage.

        Parameters
        ----------
        context:
            Existing ResolutionContext.

        Returns
        -------
        ResolutionContext

            Newly enriched immutable context.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Optional hooks
    # ---------------------------------------------------------

    def can_execute(
        self,
        context: ResolutionContext,
    ) -> bool:
        """
        Determines whether this stage should execute.

        Default implementation always returns True.

        Individual stages may override this method.
        """
        return True

    def before_execute(
        self,
        context: ResolutionContext,
    ) -> ResolutionContext:
        """
        Optional preprocessing hook.

        Default implementation returns the context unchanged.
        """
        return context

    def after_execute(
        self,
        context: ResolutionContext,
    ) -> ResolutionContext:
        """
        Optional postprocessing hook.

        Default implementation returns the context unchanged.
        """
        return context

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __call__(
        self,
        context: ResolutionContext,
    ) -> ResolutionContext:
        """
        Executes the stage as a callable.

        Pipeline implementations may simply call:

            context = stage(context)
        """

        if not self.can_execute(context):
            return context

        context = self.before_execute(context)

        context = self.execute(context)

        context = self.after_execute(context)

        return context

    def __str__(
        self,
    ) -> str:
        return self.display_text
