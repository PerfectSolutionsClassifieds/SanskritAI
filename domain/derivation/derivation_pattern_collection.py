from __future__ import annotations

"""
SanskritAI
==========

Derivation Pattern Collection

Defines the immutable collection of DerivationPattern objects.

This mirrors the collection patterns used across the Dhatu,
Pratyaya, Samasa, Grammar, and Phonology kernels.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.derivation.derivation_pattern import DerivationPattern


@dataclass(frozen=True, slots=True)
class DerivationPatternCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of derivation patterns.
    """

    patterns: tuple[DerivationPattern, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Derivation Pattern Collection"

    @property
    def display_text(self) -> str:
        return f"{len(self.patterns)} Patterns"

    @property
    def display_description(self) -> str:
        return "Immutable collection of derivation patterns."

    @property
    def count(self) -> int:
        return len(self.patterns)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> DerivationPattern | None:
        if self.is_empty:
            return None
        return self.patterns[0]

    @property
    def last(self) -> DerivationPattern | None:
        if self.is_empty:
            return None
        return self.patterns[-1]

    def add(
        self,
        pattern: DerivationPattern,
    ) -> "DerivationPatternCollection":
        """
        Returns a new collection with the supplied pattern appended.
        """
        return DerivationPatternCollection(
            patterns=self.patterns + (pattern,),
        )

    def extend(
        self,
        other: "DerivationPatternCollection",
    ) -> "DerivationPatternCollection":
        """
        Returns a new collection containing patterns from both collections.
        """
        return DerivationPatternCollection(
            patterns=self.patterns + other.patterns,
        )

    def get_by_identifier(
        self,
        identifier: str,
    ) -> DerivationPattern | None:
        """
        Returns the pattern matching the supplied identifier.
        """
        for pattern in self.patterns:
            if pattern.identifier == identifier:
                return pattern
        return None

    def find_by_category(
        self,
        category: str,
    ) -> "DerivationPatternCollection":
        """
        Returns all patterns matching the supplied category.
        """
        return DerivationPatternCollection(
            patterns=tuple(
                pattern
                for pattern in self.patterns
                if pattern.category == category
            )
        )

    def search(
        self,
        query: str,
    ) -> "DerivationPatternCollection":
        """
        Performs a simple case-insensitive search across name,
        template, description, category, and notes.
        """
        needle = query.strip().lower()

        if not needle:
            return self

        return DerivationPatternCollection(
            patterns=tuple(
                pattern
                for pattern in self.patterns
                if needle in pattern.name.lower()
                or needle in pattern.template.lower()
                or needle in pattern.description.lower()
                or needle in pattern.category.lower()
                or needle in pattern.notes.lower()
            )
        )

    def __iter__(self) -> Iterator[DerivationPattern]:
        return iter(self.patterns)

    def __len__(self) -> int:
        return len(self.patterns)

    def __getitem__(self, index: int) -> DerivationPattern:
        return self.patterns[index]

    def __str__(self) -> str:
        return self.display_text
