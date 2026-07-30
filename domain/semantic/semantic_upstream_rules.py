from __future__ import annotations

"""
SanskritAI
==========

Semantic Upstream Rules

Provides semantic rules that convert upstream kernel outputs
into structured semantic frames.

Version
-------
v1.0.0
"""

from typing import Any

from SanskritAI.domain.semantic.semantic_context import SemanticContext
from SanskritAI.domain.semantic.semantic_frame_builder import (
    SemanticFrameBuilder,
)
from SanskritAI.domain.semantic.semantic_rule import SemanticRule


class _UpstreamFrameRule(SemanticRule):
    """
    Helper base class for upstream-to-frame semantic rules.
    """

    metadata_key: str = ""
    label: str = ""
    role: str = ""

    def __init__(self) -> None:
        self._builder = SemanticFrameBuilder()

    def applies_to(self, context: SemanticContext) -> bool:
        return context.get(self.metadata_key, None) is not None

    def _frame(self, context: SemanticContext, value: Any):
        return self._builder.from_upstream(
            identifier=f"{context.identifier}:{self.metadata_key}",
            label=self.label,
            upstream=value,
            role=self.role,
            confidence=float(context.get("confidence", 0.90)),
            notes=f"Built from {self.metadata_key} output.",
        )

    def apply(self, context: SemanticContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        value = context.get(self.metadata_key)

        frame = self._frame(context, value)

        return (
            {
                "type": self.__class__.__name__,
                "text": frame.summary,
                "meaning": frame.display_description,
                "confidence": frame.confidence,
                "matched_rule": self.display_name,
                "notes": frame.notes,
                "frame": frame,
                "concepts": frame.concepts,
                "relations": frame.relations,
            },
        )


class VakyaSemanticFrameRule(_UpstreamFrameRule):
    metadata_key = "vakya"
    label = "Vakya Meaning Frame"
    role = "sentence"

    @property
    def display_name(self) -> str:
        return "Vakya Semantic Frame Rule"

    @property
    def display_description(self) -> str:
        return "Converts Vakya output into a semantic frame."


class DerivationSemanticFrameRule(_UpstreamFrameRule):
    metadata_key = "derivation"
    label = "Derivation Meaning Frame"
    role = "derives-from"

    @property
    def display_name(self) -> str:
        return "Derivation Semantic Frame Rule"

    @property
    def display_description(self) -> str:
        return "Converts Derivation output into a semantic frame."


class SamasaSemanticFrameRule(_UpstreamFrameRule):
    metadata_key = "samasa"
    label = "Samasa Meaning Frame"
    role = "compound"

    @property
    def display_name(self) -> str:
        return "Samasa Semantic Frame Rule"

    @property
    def display_description(self) -> str:
        return "Converts Samasa output into a semantic frame."


class GrammarSemanticFrameRule(_UpstreamFrameRule):
    metadata_key = "grammar"
    label = "Grammar Meaning Frame"
    role = "grammatical"

    @property
    def display_name(self) -> str:
        return "Grammar Semantic Frame Rule"

    @property
    def display_description(self) -> str:
        return "Converts Grammar output into a semantic frame."
