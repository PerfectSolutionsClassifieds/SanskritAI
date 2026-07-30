from __future__ import annotations

"""
SanskritAI
==========

Alankara Analysis

Represents one candidate figure-of-speech analysis.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AlankaraAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Alankara analysis candidate.
    """

    identifier: str

    text: str

    alankara: str = ""

    alankara_class: str = ""

    confidence: float = 1.0

    matched_rule: str = ""

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.alankara or "Alankara Analysis"

    @property
    def display_text(self) -> str:
        return self.text

    @property
    def display_description(self) -> str:
        return self.notes or self.alankara_class

    @property
    def has_alankara(self) -> bool:
        return bool(self.alankara)

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    @property
    def has_rule(self) -> bool:
        return bool(self.matched_rule)

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    def __str__(self) -> str:
        return self.display_text
