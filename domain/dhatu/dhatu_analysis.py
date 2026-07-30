from __future__ import annotations

"""
SanskritAI
==========

Dhatu Analysis

Represents one candidate analysis of a Sanskrit verbal root.

Unlike Dhatu itself (which is lexical knowledge), DhatuAnalysis
represents one interpretation produced by the Dhatu Kernel.

Future versions may include:

    • Dhatu

    • Gana

    • Pada

    • Meaning

    • Root confidence

    • Matching rule

    • Derivational notes

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.dhatu.dhatu import Dhatu


@dataclass(frozen=True, slots=True)
class DhatuAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    One Dhatu analysis candidate.
    """

    dhatu: Dhatu

    confidence: float = 1.0

    matched_rule: str = ""

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.dhatu.display_name

    @property
    def display_text(self) -> str:
        return self.dhatu.display_text

    @property
    def display_description(self) -> str:
        return self.notes or self.dhatu.display_description

    @property
    def has_rule(self) -> bool:
        return bool(self.matched_rule)

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    def __str__(self) -> str:
        return self.display_text
