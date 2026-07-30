from __future__ import annotations

"""
SanskritAI
==========

Chandas Rule

Defines the abstract foundation for Chandas rules.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.chandas.chandas_context import ChandasContext


class ChandasRule(
    ABC,
    Displayable,
):
    """
    Abstract Chandas rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Chandas rule."

    @abstractmethod
    def applies_to(self, context: ChandasContext) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, context: ChandasContext) -> tuple[Any, ...]:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text


class MeterHintRule(ChandasRule):
    """
    Recognizes explicit meter hints from metadata.
    """

    @property
    def display_name(self) -> str:
        return "Meter Hint Rule"

    @property
    def display_description(self) -> str:
        return "Uses explicit meter hints from metadata."

    def applies_to(self, context: ChandasContext) -> bool:
        return bool(
            context.get("meter", "")
            or context.get("meter_hint", "")
            or context.get("chandas_hint", "")
        )

    def apply(self, context: ChandasContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        meter = str(
            context.get("meter", "")
            or context.get("meter_hint", "")
            or context.get("chandas_hint", "")
        ).strip()

        text = str(context.subject).strip()

        return (
            {
                "type": "MeterHint",
                "text": text,
                "meter": meter,
                "meter_class": str(context.get("meter_class", "")).strip(),
                "syllable_count": int(context.get("syllable_count", 0) or 0),
                "pada_count": int(context.get("pada_count", 0) or 0),
                "confidence": float(context.get("confidence", 0.95)),
                "matched_rule": self.display_name,
                "notes": str(context.get("meter_note", "")).strip(),
            },
        )


class VerseHeuristicRule(ChandasRule):
    """
    Lightweight heuristic meter rule based on verse-like
    syllable counting and danda/pada segmentation.
    """

    _VOWELS: tuple[str, ...] = (
        "अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ॠ", "ऌ", "ॡ",
        "ए", "ऐ", "ओ", "औ",
        "ा", "ि", "ी", "ु", "ू", "ृ", "ॄ", "ॢ", "ॣ",
        "े", "ै", "ो", "ौ",
    )

    @property
    def display_name(self) -> str:
        return "Verse Heuristic Rule"

    @property
    def display_description(self) -> str:
        return "Estimates meter using lightweight verse heuristics."

    def _count_syllables(self, text: str) -> int:
        count = 0
        for ch in text:
            if ch in self._VOWELS:
                count += 1
        return count

    def _count_padas(self, text: str) -> int:
        parts = [
            part.strip()
            for part in text.replace("॥", "|").replace("।", "|").split("|")
            if part.strip()
        ]
        return len(parts) if parts else 1

    def _meter_from_syllables(self, syllables: int, pada_count: int) -> str:
        if syllables == 32 and pada_count >= 4:
            return "anuṣṭubh"
        if syllables == 48 and pada_count >= 4:
            return "bṛhatī"
        if syllables == 56 and pada_count >= 4:
            return "paṅkti"
        if syllables == 64 and pada_count >= 4:
            return "jagatī"
        return "unknown"

    def applies_to(self, context: ChandasContext) -> bool:
        return bool(str(context.subject).strip())

    def apply(self, context: ChandasContext) -> tuple[Any, ...]:
        text = str(context.subject).strip()
        if not text:
            return tuple()

        syllables = int(context.get("syllable_count", 0) or 0)
        if syllables <= 0:
            syllables = self._count_syllables(text)

        pada_count = int(context.get("pada_count", 0) or 0)
        if pada_count <= 0:
            pada_count = self._count_padas(text)

        meter = str(context.get("meter", "") or "").strip()
        if not meter:
            meter = self._meter_from_syllables(syllables, pada_count)

        return (
            {
                "type": "VerseHeuristic",
                "text": text,
                "meter": meter,
                "meter_class": str(context.get("meter_class", "")).strip(),
                "syllable_count": syllables,
                "pada_count": pada_count,
                "confidence": float(context.get("confidence", 0.75)),
                "matched_rule": self.display_name,
                "notes": f"Estimated from {syllables} syllables and {pada_count} padas.",
            },
        )
