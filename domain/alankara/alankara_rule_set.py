from __future__ import annotations

"""
SanskritAI
==========

Alankara Rule Set

Defines an immutable collection of Alankara rules.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.domain.alankara.alankara_context import AlankaraContext
from SanskritAI.domain.alankara.alankara_rule import AlankaraRule


@dataclass(frozen=True, slots=True)
class AlankaraRuleSet(
    Immutable,
    Displayable,
):
    """
    Immutable collection of Alankara rules.
    """

    rules: tuple[AlankaraRule, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Alankara Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Alankara Rules"

    @property
    def display_description(self) -> str:
        return "Immutable collection of Alankara rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(self, rule: AlankaraRule) -> "AlankaraRuleSet":
        return AlankaraRuleSet(rules=self.rules + (rule,))

    def _candidate_key(self, candidate: Any) -> str:
        if isinstance(candidate, dict):
            return repr(tuple(sorted(candidate.items())))
        return repr(candidate)

    def apply(self, context: AlankaraContext) -> tuple[Any, ...]:
        candidates: list[Any] = []
        seen: set[str] = set()

        for rule in self.rules:
            if rule.applies_to(context):
                for candidate in rule.apply(context):
                    key = self._candidate_key(candidate)
                    if key in seen:
                        continue
                    seen.add(key)
                    candidates.append(candidate)

        return tuple(candidates)

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self) -> Iterator[AlankaraRule]:
        return iter(self.rules)

    def __getitem__(self, index: int) -> AlankaraRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
