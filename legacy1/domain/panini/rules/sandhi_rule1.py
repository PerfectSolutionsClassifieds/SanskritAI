from __future__ import annotations

"""
SanskritAI
==========

Sandhi Rule

Abstract base class for every Paninian Sandhi rule.

Purpose
-------
Sandhi rules perform phonological transformations occurring
at the junction of sounds.

Typical operations include

    • vowel sandhi
    • consonant sandhi
    • visarga sandhi
    • anusvāra transformations
    • yaṇ, guṇa and vṛddhi substitutions
    • phonological assimilation

Examples

    6.1.77 iko yaṇ aci

    6.1.78 eco'yavāyāvaḥ

    8.3.15 kharavasānayor visarjanīyaḥ

Architecture
------------

PaninianRule
      │
      ▼
VidhiRule
      │
      ▼
SandhiRule
      │
      ▼
Concrete Sandhi Sūtras

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
class SandhiRule(
    VidhiRule,
    ABC,
):
    """
    Canonical abstract base class for all Sandhi rules.
    """

    def __post_init__(self) -> None:

        canonical = replace(
            self.metadata,
            category=PaninianRuleCategory.SANDHI,
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
    def is_phonological_rule(self) -> bool:
        return True

    @property
    def transforms_sound(self) -> bool:
        return True

    @property
    def operates_on_boundaries(self) -> bool:
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
        Performs the Sandhi transformation.
        """
        raise NotImplementedError
