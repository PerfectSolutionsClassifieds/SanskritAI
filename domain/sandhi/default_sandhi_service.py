from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Service

Default implementation of the SandhiService.

This class delegates all knowledge access to the configured
SandhiRepository.

Relationship
------------

SandhiResolutionKernel
        │
        ▼
DefaultSandhiService
        │
        ▼
DefaultSandhiRepository

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.sandhi.default_sandhi_repository import (
    DefaultSandhiRepository,
)

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)

from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)

from SanskritAI.domain.sandhi.sandhi_service import (
    SandhiService,
)


@dataclass(frozen=True, slots=True)
class DefaultSandhiService(
    SandhiService,
):
    """
    Default Sandhi service.
    """

    _repository: SandhiRepository = field(
        default_factory=DefaultSandhiRepository,
    )

    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Default Sandhi Service"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Default service providing access to canonical "
            "Sandhi rules."
        )

    # ---------------------------------------------------------

    @property
    def repository(
        self,
    ) -> SandhiRepository:
        return self._repository

    # ---------------------------------------------------------

    def get_rule(
        self,
        identifier: str,
    ) -> SandhiRule | None:

        return self.repository.get(identifier)

    def search_rules(
        self,
        query: str,
    ) -> SandhiRuleSet:

        return self.repository.search(query)

    def all_rules(
        self,
    ) -> SandhiRuleSet:

        return self.repository.all()

    @property
    def rule_count(
        self,
    ) -> int:

        return self.repository.count
