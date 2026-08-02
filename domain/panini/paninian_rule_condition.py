from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Condition

Defines the canonical abstraction for every condition used by
the Paninian Rule Matching Framework.

Purpose
-------
A Paninian rule is composed of two orthogonal parts:

    1. Condition(s)
    2. Transformation

Conditions determine whether a rule is applicable within the
current derivational context.

Examples
--------

6.1.77 iko yaṇ aci

Conditions

    • preceding sound ∈ ik
    • following sound ∈ ac

Transformation

    • replace ik → yaṇ

Likewise,

1.3.9 tasya lopaḥ

Condition

    • symbol possesses It-saṃjñā

Transformation

    • delete the It marker

Architecture
------------

PaninianRule
       │
       ▼
PaninianRuleMatcher
       │
       ├── evaluates
       ▼
PaninianRuleCondition(s)
       │
       ▼
PaninianRuleMatchResult

Version
-------
v1.0.0
"""

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class PaninianRuleCondition(
    ValueObject,
    Immutable,
    Displayable,
    ABC,
):
    """
    Canonical abstract Paninian rule condition.
    """

    name: str

    description: str = ""

    priority: int = 100

    enabled: bool = True

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    # ---------------------------------------------------------
    # Classification
    # ---------------------------------------------------------

    @property
    def is_enabled(self) -> bool:
        return self.enabled

    # ---------------------------------------------------------
    # Matching
    # ---------------------------------------------------------

    @abstractmethod
    def evaluate(
        self,
        context: Any,
    ) -> bool:
        """
        Evaluates this condition against a derivation context.

        Returns
        -------
        bool

        True if the condition is satisfied.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def supports(
        self,
        context: Any,
    ) -> bool:
        """
        Alias for evaluate().
        """
        return self.evaluate(context)

    # ---------------------------------------------------------
    # Ordering
    # ---------------------------------------------------------

    def __lt__(
        self,
        other: "PaninianRuleCondition",
    ) -> bool:
        return self.priority < other.priority

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(self) -> str:
        return self.display_text
