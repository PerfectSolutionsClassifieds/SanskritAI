from __future__ import annotations

"""
SanskritAI
==========

Alankara Rule

Defines the abstract foundation for Alankara rules.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.alankara.alankara_context import AlankaraContext


class AlankaraRule(
    ABC,
    Displayable,
):
    """
    Abstract Alankara rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Alankara rule."

    @abstractmethod
    def applies_to(self, context: AlankaraContext) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, context: AlankaraContext) -> tuple[Any, ...]:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text


class UpamaRule(AlankaraRule):
    """
    Detects simple simile markers and comparisons.
    """

    _MARKERS: tuple[str, ...] = (
        "इव",
        "यथा",
        "सदृश",
        "तुल्य",
        "like",
        "as",
    )

    @property
    def display_name(self) -> str:
        return "Upama Rule"

    @property
    def display_description(self) -> str:
        return "Recognizes simile-like comparison markers."

    def applies_to(self, context: AlankaraContext) -> bool:
        text = str(context.subject).strip().lower()
        return any(marker.lower() in text for marker in self._MARKERS)

    def apply(self, context: AlankaraContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = str(context.subject).strip()
        return (
            {
                "type": "Upama",
                "text": text,
                "alankara": "Upamā",
                "alankara_class": "comparison",
                "confidence": 0.90,
                "matched_rule": self.display_name,
                "notes": "Simile/comparison markers detected.",
            },
        )


class RupakaRule(AlankaraRule):
    """
    Detects metaphor-like identity expressions.
    """

    _MARKERS: tuple[str, ...] = (
        "iva na",
        "as if",
        "is",
        "इव न",
        "रूपक",
    )

    @property
    def display_name(self) -> str:
        return "Rupaka Rule"

    @property
    def display_description(self) -> str:
        return "Recognizes metaphor-like identity patterns."

    def applies_to(self, context: AlankaraContext) -> bool:
        text = str(context.subject).strip().lower()
        if any(marker.lower() in text for marker in self._MARKERS):
            return True
        return bool(context.get("alankara_hint", "").lower() in {"rupaka", "rūpaka"})

    def apply(self, context: AlankaraContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = str(context.subject).strip()
        return (
            {
                "type": "Rupaka",
                "text": text,
                "alankara": "Rūpaka",
                "alankara_class": "metaphor",
                "confidence": 0.85,
                "matched_rule": self.display_name,
                "notes": "Metaphor-like identity detected heuristically.",
            },
        )


class AnuprasaRule(AlankaraRule):
    """
    Detects repetition/alliteration-like patterns.
    """

    @property
    def display_name(self) -> str:
        return "Anuprasa Rule"

    @property
    def display_description(self) -> str:
        return "Recognizes repeated sound patterns."

    def applies_to(self, context: AlankaraContext) -> bool:
        text = str(context.subject).strip()
        tokens = [token for token in text.split() if token]
        if len(tokens) < 2:
            return False
        first_chars = [token[0] for token in tokens if token]
        return len(set(first_chars)) <= max(1, len(first_chars) // 2)

    def apply(self, context: AlankaraContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = str(context.subject).strip()
        return (
            {
                "type": "Anuprasa",
                "text": text,
                "alankara": "Anuprāsa",
                "alankara_class": "alliteration",
                "confidence": 0.72,
                "matched_rule": self.display_name,
                "notes": "Repeated initial sounds detected heuristically.",
            },
        )


class YamakaRule(AlankaraRule):
    """
    Detects repetition of the same word/segment.
    """

    @property
    def display_name(self) -> str:
        return "Yamaka Rule"

    @property
    def display_description(self) -> str:
        return "Recognizes repeated words or segments."

    def applies_to(self, context: AlankaraContext) -> bool:
        text = str(context.subject).strip()
        tokens = [token for token in text.split() if token]
        return len(tokens) >= 2 and len(set(tokens)) < len(tokens)

    def apply(self, context: AlankaraContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = str(context.subject).strip()
        return (
            {
                "type": "Yamaka",
                "text": text,
                "alankara": "Yamaka",
                "alankara_class": "repetition",
                "confidence": 0.70,
                "matched_rule": self.display_name,
                "notes": "Repeated tokens detected heuristically.",
            },
        )


class ShleshaRule(AlankaraRule):
    """
    Detects multi-meaning / ambiguity-like expressions.
    """

    _MARKERS: tuple[str, ...] = (
        "श्लेष",
        "double",
        "multiple meanings",
        "अर्थ",
    )

    @property
    def display_name(self) -> str:
        return "Shlesha Rule"

    @property
    def display_description(self) -> str:
        return "Recognizes ambiguity or multi-meaning patterns."

    def applies_to(self, context: AlankaraContext) -> bool:
        text = str(context.subject).strip().lower()
        if any(marker.lower() in text for marker in self._MARKERS):
            return True
        return bool(context.get("alankara_hint", "").lower() in {"shlesha", "śleṣa"})

    def apply(self, context: AlankaraContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = str(context.subject).strip()
        return (
            {
                "type": "Shlesha",
                "text": text,
                "alankara": "Śleṣa",
                "alankara_class": "ambiguity",
                "confidence": 0.78,
                "matched_rule": self.display_name,
                "notes": "Ambiguity/multiple-meaning hints detected.",
            },
        )
