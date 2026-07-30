from __future__ import annotations

"""
SanskritAI
==========

Semantic Analysis

Represents one candidate meaning analysis of a Sanskrit
expression.

This is the first structured meaning object for the Semantic
Kernel and will later support:
    • concept mapping
    • relation extraction
    • semantic frames
    • ontology linking

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class SemanticAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable semantic analysis candidate.
    """

    identifier: str

    text: str

    meaning: str = ""

    semantic_type: str = ""

    confidence: float = 1.0

    matched_rule: str = ""

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.semantic_type or "Semantic Analysis"

    @property
    def display_text(self) -> str:
        return self.text

    @property
    def display_description(self) -> str:
        return self.notes or self.meaning

    @property
    def has_meaning(self) -> bool:
        return bool(self.meaning)

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
