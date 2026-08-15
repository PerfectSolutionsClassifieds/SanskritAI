from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Rule Set

Defines an immutable collection of Pratyaya rules.

A PratyayaRuleSet evaluates every registered PratyayaRule and
collects candidate affix analyses.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.domain.pratyaya.pratyaya_context import PratyayaContext
from SanskritAI.domain.pratyaya.pratyaya_rule import PratyayaRule


@dataclass(frozen=True, slots=True)
class PratyayaRuleSet(
    Immutable,
    Displayable,
):
    """
    Immutable collection of Pratyaya rules.
    """

    rules: tuple[PratyayaRule, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Pratyaya Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Pratyaya Rules"

    @property
    def display_description(self) -> str:
        return "Immutable collection of Pratyaya rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(
        self,
        rule: PratyayaRule,
    ) -> "PratyayaRuleSet":
        """
        Returns a new rule set containing the supplied rule.
        """
        return PratyayaRuleSet(
            rules=self.rules + (rule,),
        )

    def apply(
        self,
        context: PratyayaContext,
    ) -> tuple[Any, ...]:
        """
        Applies every matching Pratyaya rule and returns unique
        candidates in insertion order.
        """
        candidates: list[Any] = []

        for rule in self.rules:
            if rule.applies_to(context):
                candidates.extend(rule.apply(context))

        return tuple(dict.fromkeys(candidates))

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self) -> Iterator[PratyayaRule]:
        return iter(self.rules)

    def __getitem__(self, index: int) -> PratyayaRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
