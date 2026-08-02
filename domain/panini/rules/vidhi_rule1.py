from __future__ import annotations

"""
SanskritAI
==========

Vidhi Rule

Abstract base class for every Paninian Vidhi (prescriptive /
operative) rule.

Purpose
-------
Vidhi rules constitute the primary operational rules of the
Aṣṭādhyāyī. They prescribe grammatical operations such as

    • affixation
    • substitution
    • augmentation
    • inflection
    • derivational transformations

Unlike Saṃjñā rules, Vidhi rules actively transform the
derivation.

Examples
--------

    3.1.68  kartari śap

    3.2.123 ...

Architecture
------------

PaninianRule
      │
      ▼
VidhiRule
      │
      ├── KrtRule
      ├── TaddhitaRule
      ├── StriRule
      ├── PratyayaRule
      ├── AgamaRule
      ├── AdeshaRule
      └── ...

Every concrete operational sūtra eventually derives from one
of these specialized subclasses.

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import replace
from typing import Any

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)
from SanskritAI.domain.panini.paninian_rule_category import (
    PaninianRuleCategory,
)
from SanskritAI.domain.panini.paninian_rule_metadata import (
    PaninianRuleMetadata,
)
from SanskritAI.domain.panini.paninian_rule_priority import (
    PaninianRulePriority,
)
from SanskritAI.domain.panini.paninian_rule_type import (
    PaninianRuleType,
)


@dataclass(frozen=True, slots=True)
class VidhiRule(
    PaninianRule,
    ABC,
):
    """
    Canonical abstract base class for all Vidhi rules.
    """

    def __post_init__(self) -> None:
        """
        Enforces canonical Vidhi metadata.
        """

        canonical_metadata = replace(
            self.metadata,
            category=PaninianRuleCategory.GENERAL,
            rule_type=PaninianRuleType.MANDATORY,
            priority=PaninianRulePriority.UTSARGA,
        )

        object.__setattr__(
            self,
            "metadata",
            canonical_metadata,
        )

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @property
    def is_operational_rule(self) -> bool:
        """
        Vidhi rules actively transform the derivation.
        """
        return True

    @property
    def establishes_technical_term(self) -> bool:
        return False

    @property
    def performs_transformation(self) -> bool:
        return True

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        context: Any,
    ) -> bool:
        """
        Default validation.

        Concrete subclasses may strengthen this.
        """
        return True

    # ---------------------------------------------------------
    # Hooks
    # ---------------------------------------------------------

    def before_apply(
        self,
        context: Any,
    ) -> Any:
        """
        Hook executed immediately before the grammatical
        transformation.
        """
        return context

    def after_apply(
        self,
        context: Any,
        result: tuple[Any, ...],
    ) -> tuple[Any, ...]:
        """
        Hook executed immediately after transformation.
        """
        return result

    # ---------------------------------------------------------
    # Transformation
    # ---------------------------------------------------------

    @abstractmethod
    def apply(
        self,
        context: Any,
    ) -> tuple[Any, ...]:
        """
        Executes the grammatical prescription.

        Returns
        -------
        tuple[Any, ...]

        Zero or more candidate derivations.
        """
        raise NotImplementedError
