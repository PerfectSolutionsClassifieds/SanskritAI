from __future__ import annotations

"""
SanskritAI
==========

Default Samāsa Service

Default application service backed by the canonical
Samāsa repository.

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.samasa.default_samasa_repository import (
    DefaultSamasaRepository,
)

from SanskritAI.domain.samasa.samasa_repository import (
    SamasaRepository,
)

from SanskritAI.domain.samasa.samasa_rule import SamasaRule
from SanskritAI.domain.samasa.samasa_rule_set import SamasaRuleSet

from SanskritAI.domain.samasa.samasa_service import (
    SamasaService,
)


@dataclass(frozen=True, slots=True)
class DefaultSamasaService(
    SamasaService,
):
    """
    Default Samāsa service.
    """

    _repository: SamasaRepository = field(
        default_factory=DefaultSamasaRepository,
    )

    @property
    def display_name(self) -> str:
        return "Default Samāsa Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Application service providing canonical Samāsa knowledge."
        )

    @property
    def repository(
        self,
    ) -> SamasaRepository:
        return self._repository

    def get_rule(
        self,
        identifier: str,
    ) -> SamasaRule | None:

        return self.repository.get(identifier)

    def search_rules(
        self,
        query: str,
    ) -> SamasaRuleSet:

        return self.repository.search(query)

    def all_rules(
        self,
    ) -> SamasaRuleSet:

        return self.repository.all()

    @property
    def rule_count(
        self,
    ) -> int:

        return self.repository.count
