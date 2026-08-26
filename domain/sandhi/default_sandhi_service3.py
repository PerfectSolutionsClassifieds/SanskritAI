from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Service

Default implementation of SandhiService.

The service is the composition boundary between the
application-facing Sandhi API and the canonical Sandhi
repository.

Architecture
------------

DefaultSandhiService
        │
        ▼
DefaultSandhiRepository
        │
        ▼
Canonical SandhiRuleSet

The repository itself remains empty when directly
constructed. The service supplies the canonical default
rule set when no repository is explicitly provided.

An explicitly supplied repository is always respected.

Version
-------
v1.1.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.domain.sandhi.default_sandhi_repository import (
    DefaultSandhiRepository,
)

from SanskritAI.domain.sandhi.default_sandhi_rule_set import (
    default_sandhi_rule_set,
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


def _default_sandhi_repository() -> SandhiRepository:
    """
    Constructs the canonical repository used by the default
    Sandhi service.

    This composition function deliberately keeps the
    DefaultSandhiRepository itself empty by default.

    Therefore:

        DefaultSandhiRepository()
            -> empty repository

        DefaultSandhiService()
            -> canonical repository containing the
               default Sandhi rules
    """

    return DefaultSandhiRepository(
        rule_set=default_sandhi_rule_set(),
    )


@dataclass(
    frozen=True,
    slots=True,
)
class DefaultSandhiService(
    SandhiService,
):
    """
    Canonical default Sandhi service.

    ``_repository`` remains the explicit constructor field
    because repository injection is part of the service's
    composition contract.

    Default construction receives the canonical Sandhi rule
    bundle.

    Explicit repository construction preserves the supplied
    repository unchanged.
    """

    _repository: SandhiRepository = field(
        default_factory=_default_sandhi_repository,
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
    # Repository
    # ---------------------------------------------------------

    @property
    def repository(
        self,
    ) -> SandhiRepository:

        return self._repository

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

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __str__(
        self,
    ) -> str:

        return self.display_text
