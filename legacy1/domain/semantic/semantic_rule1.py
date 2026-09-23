from __future__ import annotations

"""
SanskritAI
==========

Semantic Rule

Defines the abstract foundation for semantic rules.

A SemanticRule performs one atomic meaning-analysis operation.
Rules are intentionally independent and stateless, allowing
them to be composed into reusable SemanticRuleSets.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.semantic.semantic_context import SemanticContext


class SemanticRule(
    ABC,
    Displayable,
):
    """
    Abstract semantic rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract semantic rule."

    @abstractmethod
    def applies_to(self, context: SemanticContext) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, context: SemanticContext) -> tuple[Any, ...]:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text


class MeaningHintRule(SemanticRule):
    """
    Starter semantic rule that recognizes explicit meaning
    hints from metadata or a semantic-style textual subject.
    """

    @property
    def display_name(self) -> str:
        return "Meaning Hint Rule"

    @property
    def display_description(self) -> str:
        return "Recognizes explicit semantic hints from metadata."

    def applies_to(self, context: SemanticContext) -> bool:
        return bool(
            context.get("meaning", "")
            or context.get("semantic_hint", "")
            or context.get("concept", "")
            or context.get("sense", "")
        )

    def apply(self, context: SemanticContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = str(context.subject).strip()

        meaning = str(
            context.get("meaning", "")
            or context.get("sense", "")
            or context.get("concept", "")
        ).strip()

        semantic_type = str(
            context.get("semantic_type", "HintBasedMeaning")
        ).strip()

        return (
            {
                "type": semantic_type,
                "text": text,
                "meaning": meaning,
                "confidence": float(context.get("confidence", 0.90)),
                "matched_rule": self.display_name,
                "notes": str(context.get("semantic_note", "")).strip(),
            },
        )


class UpstreamSemanticRule(SemanticRule):
    """
    Starter rule that consumes outputs from upstream kernels
    supplied in metadata.

    Recognized metadata keys:
        - derivation
        - samasa
        - sandhi
        - grammar
        - vakya
    """

    _UPSTREAM_KEYS: tuple[str, ...] = (
        "derivation",
        "samasa",
        "sandhi",
        "grammar",
        "vakya",
    )

    @property
    def display_name(self) -> str:
        return "Upstream Semantic Rule"

    @property
    def display_description(self) -> str:
        return "Consumes upstream kernel outputs as meaning input."

    def applies_to(self, context: SemanticContext) -> bool:
        return any(key in context.metadata for key in self._UPSTREAM_KEYS)

    def _describe(self, value: Any) -> str:
        if hasattr(value, "display_text"):
            return str(getattr(value, "display_text"))
        return str(value)

    def apply(self, context: SemanticContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        parts: list[str] = []
        items: list[Any] = []

        for key in self._UPSTREAM_KEYS:
            if key not in context.metadata:
                continue

            value = context.get(key)
            items.append(value)
            parts.append(f"{key}={self._describe(value)}")

        return (
            {
                "type": "UpstreamSemantic",
                "text": str(context.subject).strip(),
                "meaning": " | ".join(parts),
                "confidence": float(context.get("confidence", 0.92)),
                "matched_rule": self.display_name,
                "notes": "Semantic interpretation assembled from upstream outputs.",
                "components": tuple(items),
            },
        )
