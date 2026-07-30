from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Analysis

Represents one candidate analysis of a Sanskrit affix.

Unlike Pratyaya itself (which is lexical/grammatical knowledge),
PratyayaAnalysis represents one interpretation produced by the
Pratyaya Kernel.

Future versions may include:

    • base Dhatu

    • semantic category

    • suffix class

    • derivational notes

    • matching rule

    • confidence ranking

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PratyayaAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    One Pratyaya analysis candidate.
    """

    identifier: str

    pratyaya: str

    transliteration: str = ""

    meaning: str = ""

    confidence: float = 1.0

    matched_rule: str = ""

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.pratyaya

    @property
    def display_text(self) -> str:
        if self.transliteration:
            return f"{self.pratyaya} ({self.transliteration})"
        return self.pratyaya

    @property
    def display_description(self) -> str:
        return self.notes or self.meaning

    @property
    def has_rule(self) -> bool:
        return bool(self.matched_rule)

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    def __str__(self) -> str:
        return self.display_text
