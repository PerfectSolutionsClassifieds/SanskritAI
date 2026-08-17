from __future__ import annotations

"""
SanskritAI
==========

Semantic Rule Set

Defines an immutable collection of Semantic rules.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.domain.semantic.semantic_context import SemanticContext
from SanskritAI.domain.semantic.semantic_rule import SemanticRule


@dataclass(frozen=True, slots=True)
class SemanticRuleSet(
    Immutable,
    Displayable,
):
    """
    Immutable collection of semantic rules.
    """

    rules: tuple[SemanticRule, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Semantic Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Semantic Rules"

    @property
    def display_description(self) -> str:
        return "Immutable collection of semantic rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(self, rule: SemanticRule) -> "SemanticRuleSet":
        return SemanticRuleSet(rules=self.rules + (rule,))

    def apply(self, context: SemanticContext) -> tuple[Any, ...]:
        candidates: list[Any] = []

        for rule in self.rules:
            if rule.applies_to(context):
                candidates.extend(rule.apply(context))

        return tuple(dict.fromkeys(candidates))

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self) -> Iterator[SemanticRule]:
        return iter(self.rules)

    def __getitem__(self, index: int) -> SemanticRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
