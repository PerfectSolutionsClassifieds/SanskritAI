from __future__ import annotations

"""
SanskritAI
==========

Vakya Rule

Defines the abstract foundation for sentence-level rules.

A VakyaRule performs one atomic sentence-analysis operation.
Rules are intentionally independent and stateless, allowing
them to be composed into reusable VakyaRuleSets.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.vakya.vakya_context import VakyaContext


class VakyaRule(
    ABC,
    Displayable,
):
    """
    Abstract sentence rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Vakya rule."

    @abstractmethod
    def applies_to(self, context: VakyaContext) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, context: VakyaContext) -> tuple[Any, ...]:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text


class UpstreamCompositionRule(
    VakyaRule,
):
    """
    Composes sentence-level analysis from upstream kernel
    outputs stored in metadata.

    Recognized metadata keys:
        - derivation
        - samasa
        - sandhi
        - grammar
    """

    @property
    def display_name(self) -> str:
        return "Upstream Composition Rule"

    @property
    def display_description(self) -> str:
        return (
            "Consumes outputs from derivation, samasa, sandhi "
            "and grammar."
        )

    def applies_to(self, context: VakyaContext) -> bool:
        return any(
            key in context.metadata
            for key in ("derivation", "samasa", "sandhi", "grammar")
        )

    def apply(self, context: VakyaContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        components = tuple(
            context.metadata[key]
            for key in ("derivation", "samasa", "sandhi", "grammar")
            if key in context.metadata
        )

        sentence = str(context.subject).strip()

        return (
            {
                "type": "UpstreamComposition",
                "sentence": sentence,
                "components": components,
                "analysis": "Sentence composed from upstream analyses.",
                "confidence": float(context.get("confidence", 0.90)),
                "matched_rule": self.display_name,
            },
        )


class StringSentenceRule(
    VakyaRule,
):
    """
    Basic rule for plain sentence strings.

    This provides a light fallback when the input is a raw
    sentence without explicit upstream metadata.
    """

    @property
    def display_name(self) -> str:
        return "String Sentence Rule"

    @property
    def display_description(self) -> str:
        return "Fallback rule for raw sentence strings."

    def applies_to(self, context: VakyaContext) -> bool:
        return bool(str(context.subject).strip())

    def apply(self, context: VakyaContext) -> tuple[Any, ...]:
        text = str(context.subject).strip()
        if not text:
            return tuple()

        tokens = tuple(token for token in text.split() if token)

        return (
            {
                "type": "StringSentence",
                "sentence": text,
                "components": tokens,
                "analysis": f"{len(tokens)} token(s)",
                "confidence": 0.75 if tokens else 0.0,
                "matched_rule": self.display_name,
            },
        )
