from __future__ import annotations

"""
SanskritAI
==========

Default Lexical Service

Canonical implementation of the LexicalService.

Responsibilities
----------------

• invokes the LexicalLookupEngine

• enriches ResolutionState

• stores LexicalResolutionResult

The service performs no lexical reasoning.

All lookup logic resides inside LexicalLookupEngine.

Architecture

ResolutionState
        │
        ▼
DefaultLexicalService
        │
        ▼
LexicalLookupEngine
        │
        ▼
CanonicalKnowledgeRepository

Version
-------
v2.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.lexical.lexical_lookup_engine import (
    LexicalLookupEngine,
)

from SanskritAI.domain.lexical.lexical_resolution_result import (
    LexicalResolutionResult,
)

from SanskritAI.domain.resolution.resolution_state import (
    ResolutionState,
)


@dataclass(frozen=True, slots=True)
class DefaultLexicalService:
    """
    Canonical lexical resolution service.
    """

    lookup_engine: LexicalLookupEngine

    @property
    def display_name(self) -> str:
        return "Default Lexical Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical lexical resolution service."
        )

    def resolve(
        self,
        state: ResolutionState,
    ) -> ResolutionState:
        """
        Performs lexical resolution and enriches the supplied
        ResolutionState.
        """

        lexical_result: LexicalResolutionResult = (
            self.lookup_engine.lookup(
                state.context,
            )
        )

        state.lexical_result = lexical_result

        state.payload = lexical_result

        if lexical_result.confidence < state.confidence:
            state.confidence = lexical_result.confidence

        return state
