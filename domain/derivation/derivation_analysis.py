from __future__ import annotations

"""
SanskritAI
==========

Derivation Analysis

Represents one candidate output of the Morphological Derivation
Kernel.

A DerivationAnalysis captures the combined result of a Dhatu
and a Pratyaya as one derivational interpretation, together
with confidence and explanatory notes.

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
class DerivationAnalysis(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable derivation analysis candidate.
    """

    identifier: str

    dhatu: Dhatu

    pratyaya: Pratyaya

    surface_form: str

    confidence: float = 1.0

    matched_rule: str = ""

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.surface_form

    @property
    def display_text(self) -> str:
        return self.surface_form

    @property
    def display_description(self) -> str:
        return self.notes or self.matched_rule

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
