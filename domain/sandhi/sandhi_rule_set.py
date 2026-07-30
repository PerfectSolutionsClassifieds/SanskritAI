from __future__ import annotations

"""
SanskritAI
==========

Sandhi Rule Set

Defines an immutable collection of Sandhi rules.

A SandhiRuleSet evaluates every registered SandhiRule and
collects the candidate Sandhi outputs.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.sandhi.sandhi_context import (
    SandhiContext,
)

from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)


@dataclass(frozen=True, slots=True)
class SandhiRuleSet(
    Immutable,
    Displayable,
):
    """
    Immutable collection of Sandhi rules.
    """

    rules: tuple[
        SandhiRule,
        ...
    ] = field(
        default_factory=tuple,
    )

    @property
    def display_name(self) -> str:
        return "Sandhi Rule Set"

    @property
    def display_text(self) -> str:
        return (
            f"{len(self.rules)} Sandhi Rules"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable collection of Sandhi rules."
        )

    @property
    def is_empty(self) -> bool:
        return len(self.rules) == 0

    @property
    def count(self) -> int:
        return len(self.rules)

    def apply(
        self,
        context: SandhiContext,
    ) -> tuple[str, ...]:
        """
        Applies every matching Sandhi rule.
        """

        candidates: list[str] = []

        for rule in self.rules:

            if rule.applies_to(context):

                candidates.extend(
                    rule.apply(context)
                )

        # Preserve insertion order while removing duplicates.

        return tuple(
            dict.fromkeys(
                candidates
            )
        )

    def add(
        self,
        rule: SandhiRule,
    ) -> "SandhiRuleSet":
        """
        Returns a new rule set containing the supplied rule.
        """

        return SandhiRuleSet(
            rules=self.rules + (rule,),
        )

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self):
        return iter(self.rules)

    def __getitem__(
        self,
        index: int,
    ) -> SandhiRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
