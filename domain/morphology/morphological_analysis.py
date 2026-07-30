from __future__ import annotations

"""
SanskritAI
==========

Morphological Analysis

Defines the immutable analysis outcome for one WordForm.

A MorphologicalAnalysis composes a WordForm with its typed
MorphologicalFeatures and adds parser provenance and
confidence information.

Relationship
------------

WordForm
    │
    ▼
MorphologicalFeatures
    │
    ▼
MorphologicalAnalysis

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.lexical.word_form import WordForm
from SanskritAI.domain.morphology.morphological_features import (
    MorphologicalFeatures,
)


@dataclass(frozen=True, slots=True)
class MorphologicalAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable morphological analysis.

    This class represents the result of analyzing one WordForm.
    """

    identifier: str

    word_form: WordForm

    features: MorphologicalFeatures

    analyzer: str = ""

    confidence: float = 1.0

    notes: str = ""

    alternatives: tuple[MorphologicalFeatures, ...] = field(
        default_factory=tuple,
    )

    @property
    def display_name(self) -> str:
        return "Morphological Analysis"

    @property
    def display_text(self) -> str:
        return (
            f"{self.word_form.display_text}"
            f" → {self.features.display_text}"
        )

    @property
    def display_description(self) -> str:
        return self.notes

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.8

    @property
    def has_alternatives(self) -> bool:
        return len(self.alternatives) > 0

    @property
    def alternative_count(self) -> int:
        return len(self.alternatives)

    @property
    def feature_count(self) -> int:
        return self.features.feature_count

    @property
    def is_nominal(self) -> bool:
        return self.features.is_nominal

    @property
    def is_verbal(self) -> bool:
        return self.features.is_verbal

    @property
    def is_indeclinable(self) -> bool:
        return self.features.is_indeclinable

    def __iter__(self) -> Iterator[MorphologicalFeatures]:
        return iter(self.alternatives)

    def __len__(self) -> int:
        return len(self.alternatives)

    def __str__(self) -> str:
        return self.display_text
