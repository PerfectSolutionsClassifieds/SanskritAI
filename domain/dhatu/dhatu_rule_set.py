from __future__ import annotations

"""
SanskritAI
==========

Dhatu Rule Set

Defines an immutable collection of Dhatu rules.

A DhatuRuleSet evaluates every registered DhatuRule and
collects candidate root analyses.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.domain.dhatu.dhatu_context import DhatuContext
from SanskritAI.domain.dhatu.dhatu_rule import DhatuRule


@dataclass(frozen=True, slots=True)
class DhatuRuleSet(
    Immutable,
    Displayable,
):
    """
    Immutable collection of Dhatu rules.
    """

    rules: tuple[DhatuRule, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Dhatu Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Dhatu Rules"

    @property
    def display_description(self) -> str:
        return "Immutable collection of Dhatu rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(
        self,
        rule: DhatuRule,
    ) -> "DhatuRuleSet":
        """
        Returns a new rule set containing the supplied rule.
        """
        return DhatuRuleSet(
            rules=self.rules + (rule,),
        )

    def apply(
        self,
        context: DhatuContext,
    ) -> tuple[Any, ...]:
        """
        Applies every matching Dhatu rule and returns unique
        candidates in insertion order.
        """
        candidates: list[Any] = []

        for rule in self.rules:
            if rule.applies_to(context):
                candidates.extend(rule.apply(context))

        return tuple(dict.fromkeys(candidates))

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self) -> Iterator[DhatuRule]:
        return iter(self.rules)

    def __getitem__(self, index: int) -> DhatuRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
