from __future__ import annotations

"""
SanskritAI
==========

Chandas Rule Set

Defines an immutable collection of Chandas rules.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Any, Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.domain.chandas.chandas_context import ChandasContext
from SanskritAI.domain.chandas.chandas_rule import ChandasRule


@dataclass(frozen=True, slots=True)
class ChandasRuleSet(
    Immutable,
    Displayable,
):
    """
    Immutable collection of Chandas rules.
    """

    rules: tuple[ChandasRule, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Chandas Rule Set"

    @property
    def display_text(self) -> str:
        return f"{len(self.rules)} Chandas Rules"

    @property
    def display_description(self) -> str:
        return "Immutable collection of Chandas rules."

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def add(self, rule: ChandasRule) -> "ChandasRuleSet":
        return ChandasRuleSet(rules=self.rules + (rule,))

    def _candidate_key(self, candidate: Any) -> str:
        if isinstance(candidate, dict):
            return repr(tuple(sorted(candidate.items())))
        return repr(candidate)

    def apply(self, context: ChandasContext) -> tuple[Any, ...]:
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

    def __iter__(self) -> Iterator[ChandasRule]:
        return iter(self.rules)

    def __getitem__(self, index: int) -> ChandasRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
