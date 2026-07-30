from __future__ import annotations

"""
SanskritAI
==========

Specific Pratyaya Rules

Provides concrete Pratyaya rules so the default bundle can
recognize a wider set of canonical affixes.

Version
-------
v1.1.0
"""

from typing import Any

from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext
from SanskritAI.domain.pratyaya.pratyaya_rule import PratyayaRule


class _ExactPratyayaRule(
    PratyayaRule,
):
    """
    Small helper base class for exact or near-exact affix rules.
    """

    pratyaya_symbol: str = ""
    transliteration_text: str = ""
    meaning_text: str = ""
    category_text: str = "krit"

    def _text(self, context: PratyayaContext) -> str:
        return str(context.subject).strip()

    def _hinted(self, context: PratyayaContext) -> bool:
        hint = str(context.get("pratyaya_hint", "")).strip().lower()
        return hint in {
            self.pratyaya_symbol.lower(),
            self.transliteration_text.lower(),
            self.display_name.lower(),
            self.__class__.__name__.lower(),
        }

    def applies_to(self, context: PratyayaContext) -> bool:
        text = self._text(context)
        if not text:
            return False

        return (
            text == self.pratyaya_symbol
            or text.endswith(self.pratyaya_symbol)
            or self._hinted(context)
        )

    def apply(self, context: PratyayaContext) -> tuple[Any, ...]:
        if not self.applies_to(context):
            return tuple()

        return (
            {
                "type": self.__class__.__name__,
                "pratyaya": self.pratyaya_symbol,
                "transliteration": self.transliteration_text,
                "meaning": self.meaning_text,
                "category": self.category_text,
                "confidence": 1.0,
                "matched_rule": self.display_name,
            },
        )


class KtaPratyayaRule(_ExactPratyayaRule):
    pratyaya_symbol = "क्त"
    transliteration_text = "kta"
    meaning_text = "past passive participle"
    category_text = "krit"

    @property
    def display_name(self) -> str:
        return "Kta Pratyaya Rule"

    @property
    def display_description(self) -> str:
        return "Concrete rule for the kta pratyaya."


class KtvaPratyayaRule(_ExactPratyayaRule):
    pratyaya_symbol = "क्त्वा"
    transliteration_text = "ktvā"
    meaning_text = "absolutive"
    category_text = "krit"

    @property
    def display_name(self) -> str:
        return "Ktva Pratyaya Rule"

    @property
    def display_description(self) -> str:
        return "Concrete rule for the ktvā pratyaya."


class TumunPratyayaRule(_ExactPratyayaRule):
    pratyaya_symbol = "तुमुन्"
    transliteration_text = "tumun"
    meaning_text = "infinitive"
    category_text = "krit"

    @property
    def display_name(self) -> str:
        return "Tumun Pratyaya Rule"

    @property
    def display_description(self) -> str:
        return "Concrete rule for the tumun pratyaya."


class LyapPratyayaRule(_ExactPratyayaRule):
    pratyaya_symbol = "ल्यप्"
    transliteration_text = "lyap"
    meaning_text = "absolutive variant"
    category_text = "krit"

    @property
    def display_name(self) -> str:
        return "Lyap Pratyaya Rule"

    @property
    def display_description(self) -> str:
        return "Concrete rule for the lyap pratyaya."


class ShatrPratyayaRule(_ExactPratyayaRule):
    pratyaya_symbol = "शतृ"
    transliteration_text = "śatṛ"
    meaning_text = "present active participle"
    category_text = "krit"

    @property
    def display_name(self) -> str:
        return "Shatr Pratyaya Rule"

    @property
    def display_description(self) -> str:
        return "Concrete rule for the śatṛ pratyaya."


class ShanacPratyayaRule(_ExactPratyayaRule):
    pratyaya_symbol = "शानच्"
    transliteration_text = "śānac"
    meaning_text = "present middle participle"
    category_text = "krit"

    @property
    def display_name(self) -> str:
        return "Shanac Pratyaya Rule"

    @property
    def display_description(self) -> str:
        return "Concrete rule for the śānac pratyaya."


class NvulPratyayaRule(_ExactPratyayaRule):
    pratyaya_symbol = "ण्वुल्"
    transliteration_text = "ṇvul"
    meaning_text = "agentive"
    category_text = "taddhita"

    @property
    def display_name(self) -> str:
        return "Nvul Pratyaya Rule"

    @property
    def display_description(self) -> str:
        return "Concrete rule for the ṇvul pratyaya."


class AniyaPratyayaRule(_ExactPratyayaRule):
    pratyaya_symbol = "अनीय"
    transliteration_text = "anīya"
    meaning_text = "desiderative / passive adjective"
    category_text = "krit"

    @property
    def display_name(self) -> str:
        return "Aniya Pratyaya Rule"

    @property
    def display_description(self) -> str:
        return "Concrete rule for the anīya pratyaya."
