from __future__ import annotations

"""
SanskritAI
==========

Derivation Pattern

Defines the canonical immutable foundation for morphological
derivation patterns.

A DerivationPattern represents a reusable derivational
blueprint such as:

    • Dhatu + Pratyaya -> Surface Form

    • Dhatu + Pratyaya + Sandhi Adjustment -> Surface Form

    • Dhatu + Pratyaya + Morphophonemic Rewrite -> Surface Form

This layer gives the Morphological Derivation Kernel a stable
place to store and reason about derivational templates rather
than only rule outputs.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class DerivationPattern(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable derivation pattern.
    """

    identifier: str

    name: str

    template: str

    description: str = ""

    category: str = ""

    priority: int = 0

    notes: str = ""

    active: bool = True

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        if self.template:
            return f"{self.name} -> {self.template}"
        return self.name

    @property
    def display_description(self) -> str:
        return self.description or self.notes

    @property
    def has_category(self) -> bool:
        return bool(self.category)

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    @property
    def is_active(self) -> bool:
        return self.active

    def __str__(self) -> str:
        return self.display_text
