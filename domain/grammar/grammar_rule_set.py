from __future__ import annotations

"""
SanskritAI
==========

Grammar Rule Set

Defines the immutable ordered collection of GrammarRule objects.

A GrammarRuleSet is used by grammar analyzers to evaluate a
subject against a sequence of grammar rules.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject
from SanskritAI.domain.grammar.grammar_rule import GrammarRule


@dataclass(frozen=True, slots=True)
class GrammarRuleSet(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable ordered collection of grammar rules.
    """

    rules: tuple[GrammarRule, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Grammar Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Rules"

    @property
    def display_description(self) -> str:
        return "Immutable ordered collection of grammar rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(
        self,
        rule: GrammarRule,
    ) -> "GrammarRuleSet":
        """
        Returns a new rule set with the supplied rule appended.
        """
        return GrammarRuleSet(
            rules=self.rules + (rule,),
        )

    def apply(
        self,
        subject: Any,
    ) -> tuple[Any, ...]:
        """
        Applies all matching rules to the supplied subject.
        """
        outputs: list[Any] = []

        for rule in self.rules:
            if rule.applies_to(subject):
                outputs.extend(rule.apply(subject))

        return tuple(outputs)

    def __iter__(self) -> Iterator[GrammarRule]:
        return iter(self.rules)

    def __len__(self) -> int:
        return len(self.rules)

    def __getitem__(
        self,
        index: int,
    ) -> GrammarRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
