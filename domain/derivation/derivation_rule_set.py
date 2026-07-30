from __future__ import annotations

"""
SanskritAI
==========

Derivation Rule Set

Defines an immutable collection of Derivation rules.

A DerivationRuleSet evaluates every registered DerivationRule
and collects candidate derivational outputs.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.domain.derivation.derivation_context import (
    DerivationContext,
)
from SanskritAI.domain.derivation.derivation_rule import DerivationRule


@dataclass(frozen=True, slots=True)
class DerivationRuleSet(
    Immutable,
    Displayable,
):
    """
    Immutable collection of derivation rules.
    """

    rules: tuple[DerivationRule, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Derivation Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Derivation Rules"

    @property
    def display_description(self) -> str:
        return "Immutable collection of derivation rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(
        self,
        rule: DerivationRule,
    ) -> "DerivationRuleSet":
        """
        Returns a new rule set containing the supplied rule.
        """
        return DerivationRuleSet(
            rules=self.rules + (rule,),
        )

    def apply(
        self,
        context: DerivationContext,
    ) -> tuple[Any, ...]:
        """
        Applies every matching derivation rule and returns
        unique candidates in insertion order.
        """
        candidates: list[Any] = []

        for rule in self.rules:
            if rule.applies_to(context):
                candidates.extend(rule.apply(context))

        return tuple(dict.fromkeys(candidates))

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self) -> Iterator[DerivationRule]:
        return iter(self.rules)

    def __getitem__(self, index: int) -> DerivationRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
