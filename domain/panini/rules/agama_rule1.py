from __future__ import annotations

"""
SanskritAI
==========

Āgama Rule

Abstract base class for every Paninian Āgama (augmentation /
insertion) rule.

Purpose
-------
Āgama rules insert additional phonemes, syllables, or
grammatical markers into an existing derivation.

Unlike Ādeśa (substitution) and Lopa (elision), an Āgama
preserves the existing linguistic material while augmenting it.

Typical applications include

    • iṭ-āgama
    • nuṭ-āgama
    • muṭ-āgama
    • augment insertion
    • auxiliary phonological insertions

Examples
--------

    7.2.xx ...

    6.x.xx ...

Architecture
------------

                PaninianRule
                       │
                       ▼
                  VidhiRule
                       │
                       ▼
                  AgamaRule
                       │
                       ▼
             Concrete Āgama Sūtras

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
class AgamaRule(
    VidhiRule,
    ABC,
):
    """
    Canonical abstract base class for all Āgama rules.
    """

    def __post_init__(self) -> None:
        """
        Canonicalizes metadata for the Āgama family.
        """

        canonical = replace(
            self.metadata,
            category=PaninianRuleCategory.AGAMA,
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
    def performs_insertion(self) -> bool:
        """
        Indicates that the rule inserts additional
        linguistic material.
        """
        return True

    @property
    def preserves_existing_form(self) -> bool:
        """
        Āgama augments rather than replaces.
        """
        return True

    @property
    def introduces_new_material(self) -> bool:
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

        Concrete Āgama rules usually strengthen this
        according to their grammatical environment.
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
        Hook executed immediately before insertion.
        """
        return context

    def after_apply(
        self,
        context: Any,
        result: tuple[Any, ...],
    ) -> tuple[Any, ...]:
        """
        Hook executed after insertion.
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
        Performs the augmentation.

        Returns
        -------
        tuple[Any, ...]

        Zero or more candidate derivations.
        """
        raise NotImplementedError
