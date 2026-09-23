
from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Service

Concrete application-facing implementation of SandhiService.

The default service composes the canonical DefaultSandhiRepository
while preserving the repository abstraction exposed by the base
SandhiService.

Architecture
------------

DefaultSandhiService
        │
        ▼
SandhiService
        │
        ▼
SandhiRepository
        │
        ▼
DefaultSandhiRepository

Version
-------
v1.1.0
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


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultSandhiService(
    SandhiService,
):
    """
    Default concrete Sandhi service.

    The inherited repository dependency is overridden with a
    canonical DefaultSandhiRepository factory.

    No second repository field is introduced.
    """

    repository: SandhiRepository = field(
        default_factory=DefaultSandhiRepository,
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Default Sandhi Service"

    @property
    def display_text(
        self,
    ) -> str:

        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:

        return (
            "Default service providing access to canonical "
            "Sandhi rules."
        )

    # ---------------------------------------------------------
    # Rule Access
    # ---------------------------------------------------------

    def get_rule(
        self,
        identifier: str,
    ) -> SandhiRule | None:

        return self.repository.get(
            identifier,
        )

    def search_rules(
        self,
        query: str,
    ) -> SandhiRuleSet:

        return self.repository.search(
            query,
        )

    def all_rules(
        self,
    ) -> SandhiRuleSet:

        return self.repository.all()

    @property
    def rule_count(
        self,
    ) -> int:

        return self.repository.count
