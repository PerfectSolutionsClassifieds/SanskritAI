from __future__ import annotations

"""
SanskritAI
==========

Dhatu

Defines the canonical immutable Sanskrit verbal root (धातु).

A Dhatu is the lexical root from which verbal forms are
derived.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.dhatu.dhatu_gana import DhatuGana


@dataclass(frozen=True, slots=True)
class Dhatu(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Sanskrit verbal root.
    """

    identifier: str

    root: str

    transliteration: str = ""

    meaning: str = ""

    gana: DhatuGana | None = None

    class_number: int = 0

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.root

    @property
    def display_text(self) -> str:
        if self.transliteration:
            return f"{self.root} ({self.transliteration})"
        return self.root

    @property
    def display_description(self) -> str:
        return self.meaning or self.notes

    @property
    def has_gana(self) -> bool:
        return self.gana is not None

    @property
    def has_meaning(self) -> bool:
        return bool(self.meaning)

    def __str__(self) -> str:
        return self.display_text
