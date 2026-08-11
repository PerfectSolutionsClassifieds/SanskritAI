from __future__ import annotations

"""
SanskritAI
==========

Default Lexical Resolution Strategy

Delegates lexical resolution entirely to the
LexicalLookupEngine.

Architecture
------------

ResolutionContext
        │
        ▼
DefaultLexicalResolutionStrategy
        │
        ▼
LexicalLookupEngine
        │
        ▼
CanonicalKnowledgeRepository
        │
        ▼
CanonicalDictionaryEntry
CanonicalDictionarySense

Version
-------
v2.0.0
"""

from SanskritAI.domain.lexical.lexical_lookup_engine import (
    LexicalLookupEngine,
)

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.lexical.lexical_resolution_strategy import (
    LexicalResolutionStrategy,
)

from SanskritAI.domain.resolution.resolution_context import (
    ResolutionContext,
)


class DefaultLexicalResolutionStrategy(
    LexicalResolutionStrategy,
):
    """
    Default lexical resolution strategy.

    The strategy contains no repository logic.

    It simply delegates lexical lookup to the
    LexicalLookupEngine.
    """

    def __init__(
        self,
        lookup_engine: LexicalLookupEngine,
    ) -> None:

        self._lookup_engine = lookup_engine

    # ---------------------------------------------------------
    # Lookup Engine
    # ---------------------------------------------------------

    @property
    def lookup_engine(
        self,
    ) -> LexicalLookupEngine:
        return self._lookup_engine

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def resolve(
        self,
        context: ResolutionContext,
    ) -> LexicalResolutionResult:
        """
        Resolve lexical information.

        Repository access, ranking, normalization,
        canonical lookup, ambiguity handling, etc.
        are delegated to the LexicalLookupEngine.
        """

        return self.lookup_engine.lookup(context)

    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:
        return "Default Lexical Resolution Strategy"

    @property
    def display_description(
        self,
    ) -> str:
        return (
            "Delegates lexical resolution to the "
            "LexicalLookupEngine."
        )
