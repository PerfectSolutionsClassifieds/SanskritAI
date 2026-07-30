from __future__ import annotations

"""
SanskritAI
==========

Samasa Rule Set

Defines an immutable collection of Samasa rules.

A SamasaRuleSet evaluates every registered SamasaRule and
collects candidate compound analyses.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.domain.samasa.samasa_context import SamasaContext
from SanskritAI.domain.samasa.samasa_rule import SamasaRule


@dataclass(frozen=True, slots=True)
class SamasaRuleSet(
    Immutable,
    Displayable,
):
    """
    Immutable collection of Samasa rules.
    """

    rules: tuple[SamasaRule, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Samasa Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Samasa Rules"

    @property
    def display_description(self) -> str:
        return "Immutable collection of Samasa rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(
        self,
        rule: SamasaRule,
    ) -> "SamasaRuleSet":
        """
        Returns a new rule set containing the supplied rule.
        """
        return SamasaRuleSet(
            rules=self.rules + (rule,),
        )

    def apply(
        self,
        context: SamasaContext,
    ) -> tuple[Any, ...]:
        """
        Applies every matching Samasa rule and returns
        unique candidates in insertion order.
        """
        candidates: list[Any] = []

        for rule in self.rules:
            if rule.applies_to(context):
                candidates.extend(rule.apply(context))

        return tuple(dict.fromkeys(candidates))

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self) -> Iterator[SamasaRule]:
        return iter(self.rules)

    def __getitem__(self, index: int) -> SamasaRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
