from __future__ import annotations

"""
SanskritAI
==========

Phoneme

Defines the abstract immutable foundation of every Sanskrit
phonological unit.

A Phoneme represents one atomic sound together with its
intrinsic phonological properties.

The phoneme itself is self-describing; therefore higher
layers (Classifier, Sandhi, Grammar, Morphology) should
query its properties rather than hard-code phonological
knowledge.

Hierarchy
---------

Phoneme
    │
    ├── Vowel
    ├── Consonant
    └── NonAlphabeticAyogavahaPhoneme

Version
-------
v2.0.0
"""

from abc import ABC
from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.phonology.phoneme_property import (
    PhonemeProperty,
)


@dataclass(frozen=True, slots=True)
class Phoneme(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Abstract immutable Sanskrit phoneme.
    """

    symbol: str

    transliteration: str = ""

    unicode_name: str = ""

    properties: tuple[
        PhonemeProperty,
        ...
    ] = field(
        default_factory=tuple,
    )

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    @property
    def identifier(self) -> str:
        return self.symbol

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.symbol

    @property
    def display_description(self) -> str:
        return self.transliteration

    # ---------------------------------------------------------
    # Property Queries
    # ---------------------------------------------------------

    def has_property(
        self,
        property: PhonemeProperty,
    ) -> bool:
        """
        Determines whether this phoneme possesses the
        supplied phonological property.
        """

        return property in self.properties

    # ---------------------------------------------------------

    def has_any_property(
        self,
        *properties: PhonemeProperty,
    ) -> bool:
        """
        Determines whether the phoneme possesses at least
        one of the supplied properties.
        """

        return any(
            self.has_property(prop)
            for prop in properties
        )

    # ---------------------------------------------------------

    def has_all_properties(
        self,
        *properties: PhonemeProperty,
    ) -> bool:
        """
        Determines whether the phoneme possesses every
        supplied property.
        """

        return all(
            self.has_property(prop)
            for prop in properties
        )

    # ---------------------------------------------------------

    @property
    def property_count(self) -> int:
        return len(self.properties)

    # ---------------------------------------------------------

    @property
    def is_vowel(self) -> bool:
        return False

    @property
    def is_consonant(self) -> bool:
        return False

    @property
    def is_non_alphabetic(self) -> bool:
        return False

    @property
    def is_ayogavaha(self) -> bool:
        return False

    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.symbol
