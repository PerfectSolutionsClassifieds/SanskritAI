from __future__ import annotations

"""
SanskritAI
==========

Ādeśa Rule

Abstract base class for every Paninian Ādeśa
(substitution) rule.

Purpose
-------
Ādeśa rules replace one linguistic entity with another.

Unlike

    • Āgama — inserts

    • Lopa — deletes

Ādeśa performs a grammatical substitution while preserving
the derivational continuity.

Examples
--------

    iko yaṇ aci

    eco'yavāyāvaḥ

    sasajuṣo ruḥ

Architecture
------------

            PaninianRule
                   │
                   ▼
              VidhiRule
                   │
                   ▼
             AdeshaRule
                   │
                   ▼
        Concrete Ādeśa Sūtras

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import replace
from typing import Any

from SanskritAI.domain.panini.paninian_rule_category import (
    PaninianRuleCategory,
)
from SanskritAI.domain.panini.paninian_rule_priority import (
    PaninianRulePriority,
)
from SanskritAI.domain.panini.paninian_rule_type import (
    PaninianRuleType,
)
from SanskritAI.domain.panini.rules.vidhi_rule import (
    VidhiRule,
)


@dataclass(frozen=True, slots=True)
class AdeshaRule(
    VidhiRule,
    ABC,
):
    """
    Canonical abstract base class for all Ādeśa rules.
    """

    def __post_init__(self) -> None:
        """
        Canonicalizes metadata for the Ādeśa family.
        """

        canonical = replace(
            self.metadata,
            category=PaninianRuleCategory.ADESHA,
            rule_type=PaninianRuleType.TRANSFORMATION,
            priority=PaninianRulePriority.HIGH,
        )

        object.__setattr__(
            self,
            "metadata",
            canonical,
        )

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @property
    def performs_substitution(self) -> bool:
        """
        Indicates that this rule replaces one
        grammatical entity with another.
        """
        return True

    @property
    def preserves_derivational_structure(self) -> bool:
        """
        Substitution changes linguistic realization
        while preserving grammatical identity.
        """
        return True

    @property
    def introduces_new_material(self) -> bool:
        """
        Unlike Āgama, Ādeśa does not introduce
        additional material.
        """
        return False

    @property
    def removes_material(self) -> bool:
        """
        Unlike Lopa, Ādeśa does not remove
        grammatical material.
        """
        return False

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        context: Any,
    ) -> bool:
        """
        Default validation.

        Concrete Ādeśa rules normally strengthen
        this according to their grammatical
        environment.
        """
        return True

    # ---------------------------------------------------------
    # Execution Hooks
    # ---------------------------------------------------------

    def before_apply(
        self,
        context: Any,
    ) -> Any:
        """
        Executes immediately before substitution.
        """
        return context

    def after_apply(
        self,
        context: Any,
        result: tuple[Any, ...],
    ) -> tuple[Any, ...]:
        """
        Executes immediately after substitution.
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
        Performs the grammatical substitution.

        Returns
        -------
        tuple[Any, ...]

        Zero or more candidate derivations.
        """
        raise NotImplementedError
