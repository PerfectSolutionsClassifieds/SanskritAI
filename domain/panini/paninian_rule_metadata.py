from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Metadata

Canonical immutable metadata shared by every Paninian
grammatical rule.

The metadata intentionally separates:

1. Classical rule classification
2. Grammatical operation
3. Rule semantics
4. Canonical textual sūtra identity

A PaninianRuleMetadata instance owns the canonical
PaninianSutra referenced by the executable rule.

Version
-------
v3.0.0
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

from SanskritAI.domain.panini.paninian_sutra import (
    PaninianSutra,
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
    # Canonical Sūtra
    # ---------------------------------------------------------

    sutra: PaninianSutra

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
        return self.sutra.sutra_number

    @property
    def display_text(self) -> str:
        return (
            f"{self.sutra.sutra_number}"
            " — "
            f"{self.sutra.sutra_text}"
        )

    @property
    def display_description(self) -> str:
        return (
            f"{self.category.name}"
            " / "
            f"{self.operation.name}"
        )

    # ---------------------------------------------------------
    # Classical Classification Helpers
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
    def is_adhikara(self) -> bool:
        return (
            self.category
            is PaninianRuleCategory.ADHIKARA
        )

    # ---------------------------------------------------------
    # Compatibility Helpers
    # ---------------------------------------------------------

    @property
    def is_vidhi(self) -> bool:
        """
        Current PaninianRuleCategory does not expose a VIDHI
        member. Vidhi rules are therefore represented through
        their concrete operational category.

        This property is retained as a compatibility hook.
        """

        return self.category in {
            PaninianRuleCategory.ADESHA,
            PaninianRuleCategory.AGAMA,
            PaninianRuleCategory.LOPA,
            PaninianRuleCategory.SANDHI,
            PaninianRuleCategory.TRIPADI,
            PaninianRuleCategory.GUNA_VRDDHI,
        }

    @property
    def is_niyama(self) -> bool:
        return (
            self.rule_type
            is PaninianRuleType.NIYAMA
        )

    @property
    def is_atidesha(self) -> bool:
        return (
            self.rule_type
            is PaninianRuleType.ATIDESHA
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
