from __future__ import annotations

"""
SanskritAI
==========

Default Samāsa Repository

Default in-memory repository.

Currently returns an empty canonical repository until
knowledge sources are connected.

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.domain.samasa.samasa_repository import (
    SamasaRepository,
)

from SanskritAI.domain.samasa.samasa_rule import SamasaRule
from SanskritAI.domain.samasa.samasa_rule_set import SamasaRuleSet


@dataclass(frozen=True, slots=True)
class DefaultSamasaRepository(
    SamasaRepository,
):
    """
    Default repository implementation.
    """

    _rules: SamasaRuleSet = SamasaRuleSet()

    def get(
        self,
        identifier: str,
    ) -> SamasaRule | None:

        for rule in self._rules:
            if rule.identifier == identifier:
                return rule

        return None

    def search(
        self,
        query: str,
    ) -> SamasaRuleSet:

        query = query.lower()

        matches = tuple(
            rule
            for rule in self._rules
            if query in rule.display_text.lower()
        )

        return SamasaRuleSet(
            rules=matches,
        )

    def all(
        self,
    ) -> SamasaRuleSet:

        return self._rules

    @property
    def count(
        self,
    ) -> int:

        return len(self._rules)
