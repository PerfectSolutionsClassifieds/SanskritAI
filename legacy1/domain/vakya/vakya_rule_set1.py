from __future__ import annotations

"""
SanskritAI
==========

Vakya Rule Set

Defines an immutable collection of Vakya rules.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.domain.vakya.vakya_context import VakyaContext
from SanskritAI.domain.vakya.vakya_rule import VakyaRule


@dataclass(frozen=True, slots=True)
class VakyaRuleSet(
    Immutable,
    Displayable,
):
    """
    Immutable collection of sentence rules.
    """

    rules: tuple[VakyaRule, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Vakya Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Vakya Rules"

    @property
    def display_description(self) -> str:
        return "Immutable collection of sentence rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(self, rule: VakyaRule) -> "VakyaRuleSet":
        return VakyaRuleSet(rules=self.rules + (rule,))

    def apply(self, context: VakyaContext) -> tuple[Any, ...]:
        candidates: list[Any] = []

        for rule in self.rules:
            if rule.applies_to(context):
                candidates.extend(rule.apply(context))

        return tuple(dict.fromkeys(candidates))

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self) -> Iterator[VakyaRule]:
        return iter(self.rules)

    def __getitem__(self, index: int) -> VakyaRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
