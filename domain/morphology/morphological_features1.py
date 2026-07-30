from __future__ import annotations

"""
SanskritAI
==========

Morphological Features

Defines the immutable grammatical features associated with a
WordForm.

This object represents grammatical information only.
It intentionally contains no parser-specific or analysis-
specific information.

Relationship
------------

WordForm
    │
    └── MorphologicalFeatures
            │
            └── MorphologicalAnalysis

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class MorphologicalFeatures(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable grammatical feature set.
    """

    stem: str = ""

    root: str = ""

    part_of_speech: str = ""

    gender: str = ""

    number: str = ""

    case: str = ""

    person: str = ""

    tense: str = ""

    mood: str = ""

    voice: str = ""

    pada: str = ""

    lakara: str = ""

    description: str = ""

    @property
    def display_name(self) -> str:
        return "Morphological Features"

    @property
    def display_text(self) -> str:
        components = []

        if self.part_of_speech:
            components.append(self.part_of_speech)

        if self.gender:
            components.append(self.gender)

        if self.number:
            components.append(self.number)

        if self.case:
            components.append(self.case)

        return ", ".join(components)

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def is_nominal(self) -> bool:
        return bool(self.case)

    @property
    def is_verbal(self) -> bool:
        return bool(self.lakara or self.person)

    def __str__(self) -> str:
        return self.display_text
