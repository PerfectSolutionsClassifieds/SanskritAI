from __future__ import annotations

"""
SanskritAI
==========

Vakya Analysis

Represents one candidate output of the Vakya (sentence) Kernel.

A VakyaAnalysis captures one sentence-level interpretation
derived from upstream kernel outputs such as Derivation,
Samasa, Sandhi, and Grammar.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class VakyaAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable sentence analysis candidate.
    """

    identifier: str

    sentence: str

    components: tuple[object, ...] = ()

    analysis_type: str = ""

    confidence: float = 1.0

    matched_rule: str = ""

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.sentence

    @property
    def display_text(self) -> str:
        return self.sentence

    @property
    def display_description(self) -> str:
        return self.notes or self.analysis_type

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
