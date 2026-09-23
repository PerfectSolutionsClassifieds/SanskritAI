from __future__ import annotations

"""
SanskritAI
==========

Lopa Rule

Abstract base class for every Paninian Lopa (elision /
deletion) rule.

Purpose
-------
Lopa rules remove, suppress, or render grammatical elements
non-manifest during derivation while preserving their
grammatical effects where prescribed by Pāṇini.

Typical applications include

    • It-letter deletion
    • Affix elision
    • Stem elision
    • Augment elision
    • Phonological disappearance

Examples
--------

    1.3.9   tasya lopaḥ

    together with the numerous later lopa rules of the
    Aṣṭādhyāyī.

Architecture
------------

PaninianRule
      │
      ▼
VidhiRule
      │
      ▼
LopaRule
      │
      ▼
Concrete Lopa Sūtra

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
class LopaRule(
    VidhiRule,
    ABC,
):
    """
    Canonical abstract base class for all Lopa rules.
    """

    def __post_init__(self) -> None:
        """
        Enforces canonical Lopa metadata.
        """

        canonical_metadata = replace(
            self.metadata,
            category=PaninianRuleCategory.LOPA,
            rule_type=PaninianRuleType.TRANSFORMATION,
            priority=PaninianRulePriority.HIGH,
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
    def performs_elision(self) -> bool:
        """
        Indicates that this rule removes or suppresses
        one or more grammatical entities.
        """
        return True

    @property
    def is_destructive_transformation(self) -> bool:
        """
        Lopa rules remove visible linguistic material.
        """
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

        Concrete subclasses may strengthen the
        applicability conditions.
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
        Executes immediately before the elision.
        """
        return context

    def after_apply(
        self,
        context: Any,
        result: tuple[Any, ...],
    ) -> tuple[Any, ...]:
        """
        Executes immediately after the elision.
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
        Performs the grammatical elision.

        Returns
        -------
        tuple[Any, ...]

        Zero or more candidate derivations.
        """
        raise NotImplementedError
