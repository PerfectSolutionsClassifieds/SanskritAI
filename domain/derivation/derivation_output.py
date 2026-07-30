from __future__ import annotations

"""
SanskritAI
==========

Derivation Output

Represents one concrete generated output of the Morphological
Derivation Kernel.

This is the model you can use when you want a real derived
word-form rather than only an analysis record.

Typical fields include:

    • Dhatu
    • Pratyaya
    • Surface form
    • Pada / derived word
    • Confidence
    • Pattern source
    • Notes

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.pratyaya.pratyaya_factory import Pratyaya


@dataclass(frozen=True, slots=True)
class DerivationOutput(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable morphological derivation output.
    """

    identifier: str

    dhatu: Dhatu

    pratyaya: Pratyaya

    surface_form: str

    pada: str = ""

    confidence: float = 1.0

    source_pattern: str = ""

    matched_rule: str = ""

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.surface_form or "Derivation Output"

    @property
    def display_text(self) -> str:
        if self.pada:
            return f"{self.surface_form} ({self.pada})"
        return self.surface_form

    @property
    def display_description(self) -> str:
        if self.notes:
            return self.notes
        if self.source_pattern:
            return self.source_pattern
        return ""

    @property
    def has_pada(self) -> bool:
        return bool(self.pada)

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    @property
    def has_source_pattern(self) -> bool:
        return bool(self.source_pattern)

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.80

    def __str__(self) -> str:
        return self.display_text
