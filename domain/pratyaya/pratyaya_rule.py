from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Rule

Defines the abstract foundation for every Pratyaya rule.

A PratyayaRule performs one atomic affix-analysis operation.
Rules are intentionally independent and stateless, allowing
them to be composed into reusable PratyayaRuleSets.

This module also includes the first lightweight concrete
heuristic rules so the default Pratyaya bundle can produce
useful baseline outputs.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext


class PratyayaRule(
    ABC,
    Displayable,
):
    """
    Abstract Pratyaya rule.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract Pratyaya rule."

    @abstractmethod
    def applies_to(
        self,
        context: PratyayaContext,
    ) -> bool:
        """
        Determines whether this rule applies.
        """
        raise NotImplementedError

    @abstractmethod
    def apply(
        self,
        context: PratyayaContext,
    ) -> tuple[Any, ...]:
        """
        Applies the Pratyaya rule and returns candidate outputs.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.display_text


class KnownPratyayaRule(
    PratyayaRule,
):
    """
    Lightweight heuristic rule for commonly observed Sanskrit
    affix-like endings and explicit metadata hints.

    This starter rule is intentionally conservative.
    """

    _COMMON_PRATYAYA_SUFFIXES: tuple[str, ...] = (
        "क्त",
        "क्त्वा",
        "तव्य",
        "तुमुन्",
        "ल्यप्",
        "शतृ",
        "शानच्",
        "ण्वुल्",
        "अनीय",
    )

    @property
    def display_name(self) -> str:
        return "Known Pratyaya Rule"

    @property
    def display_description(self) -> str:
        return "Heuristic rule for known Pratyaya endings."

    def _extract_text(self, context: PratyayaContext) -> str:
        return str(context.subject).strip()

    def _hinted(self, context: PratyayaContext) -> bool:
        hint = str(context.get("pratyaya_hint", "")).lower().strip()
        return hint in {"known", "pratyaya", "affix", "suffix"}

    def applies_to(
        self,
        context: PratyayaContext,
    ) -> bool:
        text = self._extract_text(context)
        if not text:
            return False

        if self._hinted(context):
            return True

        return any(
            text.endswith(suffix)
            for suffix in self._COMMON_PRATYAYA_SUFFIXES
        )

    def apply(
        self,
        context: PratyayaContext,
    ) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        text = self._extract_text(context)
        candidates: list[Any] = []

        for suffix in self._COMMON_PRATYAYA_SUFFIXES:
            if text.endswith(suffix):
                stem = text[: -len(suffix)]
                candidates.append(
                    {
                        "type": "KnownPratyaya",
                        "surface": text,
                        "stem": stem,
                        "pratyaya": suffix,
                        "analysis": f"{stem} + {suffix}",
                    }
                )

        if self._hinted(context) and not candidates:
            candidates.append(
                {
                    "type": "KnownPratyaya",
                    "surface": text,
                    "stem": str(context.get("stem", "")),
                    "pratyaya": str(context.get("pratyaya", "")),
                    "analysis": str(context.get("analysis", "")),
                }
            )

        return tuple(candidates)


class AffixHintRule(
    PratyayaRule,
):
    """
    Heuristic rule driven by explicit metadata hints.

    Useful when the caller already knows the candidate affix
    and wants the kernel to confirm/normalize it.
    """

    @property
    def display_name(self) -> str:
        return "Affix Hint Rule"

    @property
    def display_description(self) -> str:
        return "Metadata-driven Pratyaya rule."

    def applies_to(
        self,
        context: PratyayaContext,
    ) -> bool:
        return bool(context.get("pratyaya", "") or context.get("pratyaya_hint", ""))

    def apply(
        self,
        context: PratyayaContext,
    ) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        return (
            {
                "type": "PratyayaHint",
                "surface": str(context.subject).strip(),
                "stem": str(context.get("stem", "")),
                "pratyaya": str(context.get("pratyaya", "")),
                "analysis": str(context.get("analysis", "")),
            },
        )
