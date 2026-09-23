from __future__ import annotations

"""
SanskritAI
==========

Tripādī Rule

Abstract base class for every Paninian Tripādī rule.

Purpose
-------
Tripādī rules correspond to the final three chapters of the
Aṣṭādhyāyī (8.2–8.4).

These rules represent the final phonological layer of the
Paninian derivation.

They are executed after the principal derivational
morphology and often override earlier phonological states.

Typical operations include

    • final consonant changes
    • visarga transformations
    • anusvāra rules
    • external sandhi refinements
    • pronunciation adjustments

Architecture
------------

PaninianRule
      │
      ▼
SandhiRule
      │
      ▼
TripadiRule
      │
      ▼
Concrete Tripādī Sūtras

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
from SanskritAI.domain.panini.rules.sandhi_rule import (
    SandhiRule,
)


@dataclass(frozen=True, slots=True)
class TripadiRule(
    SandhiRule,
    ABC,
):
    """
    Canonical abstract base class for all Tripādī rules.
    """

    def __post_init__(self) -> None:

        canonical = replace(
            self.metadata,
            category=PaninianRuleCategory.TRIPADI,
            rule_type=PaninianRuleType.FINALIZATION,
            priority=PaninianRulePriority.HIGHEST,
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
    def is_tripadi_rule(self) -> bool:
        return True

    @property
    def executes_last(self) -> bool:
        return True

    @property
    def finalizes_phonology(self) -> bool:
        return True

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        context: Any,
    ) -> bool:
        return True

    # ---------------------------------------------------------
    # Hooks
    # ---------------------------------------------------------

    def before_apply(
        self,
        context: Any,
    ) -> Any:
        return context

    def after_apply(
        self,
        context: Any,
        result: tuple[Any, ...],
    ) -> tuple[Any, ...]:
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
        Executes the final Tripādī phonological rule.
        """
        raise NotImplementedError
