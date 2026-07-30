from __future__ import annotations

"""
SanskritAI
==========

Chandas Analysis

Represents one candidate meter analysis of a Sanskrit verse.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ChandasAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Chandas analysis candidate.
    """

    identifier: str

    text: str

    meter: str = ""

    meter_class: str = ""

    syllable_count: int = 0

    pada_count: int = 0

    confidence: float = 1.0

    matched_rule: str = ""

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.meter or "Chandas Analysis"

    @property
    def display_text(self) -> str:
        return self.text

    @property
    def display_description(self) -> str:
        return self.notes or self.meter_class

    @property
    def has_meter(self) -> bool:
        return bool(self.meter)

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
