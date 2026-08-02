from __future__ import annotations

"""
SanskritAI
==========

Saṃjñā Rule

Abstract base class for all Paninian Saṃjñā (technical
designation) rules.

Purpose
-------
Saṃjñā rules establish grammatical terminology and symbolic
identifiers used throughout the Aṣṭādhyāyī.

Examples
--------

    1.1.1  vṛddhir ādaiC

    1.1.2  adeṅ guṇaḥ

    1.3.2  upadeśe 'janunāsika it

These rules generally do not transform a form directly.
Instead they annotate the derivation with grammatical
knowledge that later rules depend upon.

Architecture
------------

PaninianRule
      │
      ▼
SamjnaRule
      │
      ▼
Concrete Saṃjñā Sūtra

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
class SamjnaRule(
    PaninianRule,
    ABC,
):
    """
    Abstract base class for every Saṃjñā rule.
    """

    def __post_init__(self) -> None:
        """
        Ensures canonical metadata classification.
        """

        canonical_metadata = replace(
            self.metadata,
            category=PaninianRuleCategory.SAMJNA,
            rule_type=PaninianRuleType.ANNOTATION,
            priority=PaninianRulePriority.PARIBHASHA,
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
    def is_annotation_rule(self) -> bool:
        return True

    @property
    def establishes_technical_term(self) -> bool:
        return True

    # ---------------------------------------------------------
    # Life-cycle
    # ---------------------------------------------------------

    def validate(
        self,
        context: Any,
    ) -> bool:
        """
        Default validation.

        Saṃjñā rules are generally applicable whenever
        their supports() predicate succeeds.
        """
        return True

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    @abstractmethod
    def apply(
        self,
        context: Any,
    ) -> tuple[Any, ...]:
        """
        Applies the Saṃjñā.

        Concrete subclasses usually annotate the
        derivation rather than performing direct
        phonological transformation.
        """
        raise NotImplementedError
