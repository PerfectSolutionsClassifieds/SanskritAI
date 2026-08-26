from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Repository

Default in-memory implementation of the canonical
SandhiRepository.

Initially the repository is intentionally empty.

Future versions will populate it from

• Pāṇinian Sandhi rules

• Siddhānta Kaumudī

• Kāśikā

• Custom SanskritAI rule databases

The repository remains read-only.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)

from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)


@dataclass(frozen=True, slots=True)
class DefaultSandhiRepository(
    SandhiRepository,
):
    """
    Default canonical Sandhi repository.
    """

    rule_set: SandhiRuleSet = field(
        default_factory=SandhiRuleSet,
    )

    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Default Sandhi Repository"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Default in-memory repository of canonical "
            "Sandhi rules."
        )

    # ---------------------------------------------------------
    # Repository API
    # ---------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> SandhiRule | None:

        for rule in self.rule_set:
            if rule.identifier == identifier:
                return rule

        return None

    def contains(
        self,
        identifier: str,
    ) -> bool:

        return self.get(identifier) is not None

    def search(
        self,
        query: str,
    ) -> SandhiRuleSet:

        query = query.lower()

        matches = tuple(
            rule
            for rule in self.rule_set
            if (
                query in rule.identifier.lower()
                or query in rule.display_text.lower()
                or query in rule.display_description.lower()
            )
        )

        return SandhiRuleSet(
            rules=matches,
        )

    def all(
        self,
    ) -> SandhiRuleSet:

        return self.rule_set

    # ---------------------------------------------------------

    @property
    def count(
        self,
    ) -> int:

        return len(self.rule_set)
