from __future__ import annotations

"""
SanskritAI
==========

Default Lexical Service
=======================

Canonical concrete implementation of LexicalService.

The DefaultLexicalService does not duplicate lexical lookup
logic. It inherits the canonical service orchestration and
therefore uses:

    LexicalService
        ↓
    LexicalLookupEngine
        ↓
    LexicalRepository
        ↓
    CanonicalKnowledgeRepository

Responsibilities
----------------
• provide the canonical LexicalService implementation
• preserve the repository-based composition-root contract
• expose the default lexical contributor to ResolutionPipeline

No lexical reasoning is implemented here.

Version
-------
v3.1.0
"""

from dataclasses import dataclass

from SanskritAI.domain.lexical.lexical_service import (
    LexicalService,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultLexicalService(
    LexicalService,
):
    """
    Canonical LexicalService implementation.

    All lexical resolution behavior is inherited from
    LexicalService.
    """

    @property
    def display_name(
        self,
    ) -> str:
        return "Default Lexical Service"

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
            "Canonical lexical resolution service."
        )

    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text
