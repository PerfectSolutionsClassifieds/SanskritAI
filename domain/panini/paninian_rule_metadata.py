from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Metadata

Canonical metadata shared by every Paninian grammatical rule.

This metadata intentionally separates two independent concepts.

1. CATEGORY
-----------

"What kind of sūtra is this?"

Examples

    • Saṃjñā
    • Paribhāṣā
    • Vidhi
    • Niyama
    • Atideśa
    • Adhikāra

This is the traditional classical classification.

2. OPERATION
------------

"What grammatical operation does this rule perform?"

Examples

    • Āgama
    • Lopa
    • Ādeśa
    • Sandhi
    • Pratyaya
    • Samāsa

A Saṃjñā rule normally has

    Operation = NONE

whereas

6.1.77

Category

    VIDHI

Operation

    ADESHA

This orthogonal design mirrors the organization of the
Aṣṭādhyāyī while remaining suitable for AI reasoning,
rule indexing and explainable derivation.

Version
-------
v2.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_rule_category import (
    PaninianRuleCategory,
)

from SanskritAI.domain.panini.paninian_rule_operation import (
    PaninianRuleOperation,
)

from SanskritAI.domain.panini.paninian_rule_priority import (
    PaninianRulePriority,
)

from SanskritAI.domain.panini.paninian_rule_type import (
    PaninianRuleType,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PaninianRuleMetadata(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Canonical immutable metadata describing a Paninian rule.
    """

    # ---------------------------------------------------------
    # Classical Classification
    # ---------------------------------------------------------

    category: PaninianRuleCategory

    # ---------------------------------------------------------
    # Operational Behaviour
    # ---------------------------------------------------------

    operation: PaninianRuleOperation = (
        PaninianRuleOperation.NONE
    )

    # ---------------------------------------------------------
    # Rule Semantics
    # ---------------------------------------------------------

    rule_type: PaninianRuleType = (
        PaninianRuleType.MANDATORY
    )

    priority: PaninianRulePriority = (
        PaninianRulePriority.NORMAL
    )

    # ---------------------------------------------------------
    # Optional Information
    # ---------------------------------------------------------

    source: str = "Aṣṭādhyāyī"

    notes: str = ""

    tags: tuple[str, ...] = field(
        default_factory=tuple,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return (
            f"{self.category.name}"
        )

    @property
    def display_text(self) -> str:
        return (
            f"{self.category.name}"
            " / "
            f"{self.operation.name}"
        )

    @property
    def display_description(self) -> str:
        return (
            f"{self.rule_type.name}"
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def is_samjna(self) -> bool:
        return (
            self.category
            is PaninianRuleCategory.SAMJNA
        )

    @property
    def is_paribhasha(self) -> bool:
        return (
            self.category
            is PaninianRuleCategory.PARIBHASHA
        )

    @property
    def is_vidhi(self) -> bool:
        return (
            self.category
            is PaninianRuleCategory.VIDHI
        )

    @property
    def is_niyama(self) -> bool:
        return (
            self.category
            is PaninianRuleCategory.NIYAMA
        )

    @property
    def is_atidesha(self) -> bool:
        return (
            self.category
            is PaninianRuleCategory.ATIDESHA
        )

    @property
    def is_adhikara(self) -> bool:
        return (
            self.category
            is PaninianRuleCategory.ADHIKARA
        )

    # ---------------------------------------------------------
    # Operation Helpers
    # ---------------------------------------------------------

    @property
    def has_operation(self) -> bool:
        return (
            self.operation
            is not PaninianRuleOperation.NONE
        )

    @property
    def is_transformational(self) -> bool:
        return self.has_operation

    @property
    def is_phonological(self) -> bool:
        return self.operation in {
            PaninianRuleOperation.SANDHI,
            PaninianRuleOperation.TRIPADI,
            PaninianRuleOperation.GUNA,
            PaninianRuleOperation.VRDDHI,
            PaninianRuleOperation.YAṆ,
        }

    @property
    def is_morphological(self) -> bool:
        return self.operation in {
            PaninianRuleOperation.AGAMA,
            PaninianRuleOperation.LOPA,
            PaninianRuleOperation.ADESHA,
            PaninianRuleOperation.PRATYAYA,
            PaninianRuleOperation.KRT,
            PaninianRuleOperation.TADDHITA,
            PaninianRuleOperation.SUP,
            PaninianRuleOperation.TIN,
            PaninianRuleOperation.VIKARANA,
            PaninianRuleOperation.DHATU,
            PaninianRuleOperation.ANGA,
        }

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
