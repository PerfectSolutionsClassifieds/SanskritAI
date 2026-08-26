from __future__ import annotations

"""
SanskritAI
==========

Default Sandhi Service

Canonical application-facing implementation of SandhiService.

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
Canonical SandhiRuleSet

Construction policy
-------------------

DefaultSandhiService()
    -> canonical default repository

DefaultSandhiService(
    _repository=repository
)
    -> explicitly supplied repository

DefaultSandhiService(
    repository=repository
)
    -> explicitly supplied repository

The repository itself remains empty when directly constructed:

    DefaultSandhiRepository()

Canonical rule population belongs to this service's
composition boundary, not to the repository itself.

Version
-------
v1.2.0
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
    Construct the canonical repository used by the default
    Sandhi service.

    This intentionally does NOT change the default behavior
    of DefaultSandhiRepository itself.
    """

    return DefaultSandhiRepository(
        rule_set=default_sandhi_rule_set(),
    )


@dataclass(
    frozen=True,
    slots=True,
    init=False,
)
class DefaultSandhiService(
    SandhiService,
):
    """
    Canonical default Sandhi service.

    The inherited ``repository`` slot remains the authoritative
    repository exposed by the service.

    ``_repository`` is retained as a constructor-compatible
    injection alias because the existing architectural tests
    and composition boundary use that form.

    Both of the following are supported:

        DefaultSandhiService()

        DefaultSandhiService(
            _repository=repository
        )

    The explicit ``repository=`` form is also supported.
    """

    # ---------------------------------------------------------
    # Private construction alias
    # ---------------------------------------------------------

    _repository: SandhiRepository = field(
        default_factory=_default_sandhi_repository,
    )

    # ---------------------------------------------------------
    # Custom immutable constructor
    # ---------------------------------------------------------

    def __init__(
        self,
        repository: SandhiRepository | None = None,
        *,
        _repository: SandhiRepository | None = None,
    ) -> None:
        """
        Construct the default Sandhi service.

        Parameters
        ----------
        repository:
            Explicit repository supplied using the public
            repository name.

        _repository:
            Backward-compatible dependency-injection alias.

        Rules
        -----

        1. No repository supplied
           -> canonical default repository.

        2. Only repository supplied
           -> use repository.

        3. Only _repository supplied
           -> use _repository.

        4. Both supplied
           -> they must refer to the same repository.

        The object remains frozen and slot-based.
        """

        if (
            repository is not None
            and _repository is not None
            and repository is not _repository
        ):
            raise ValueError(
                "repository and _repository must refer "
                "to the same repository when both are supplied."
            )

        selected_repository = (
            repository
            if repository is not None
            else _repository
        )

        if selected_repository is None:
            selected_repository = (
                _default_sandhi_repository()
            )

        # The inherited SandhiService.repository slot is the
        # canonical public repository reference.
        object.__setattr__(
            self,
            "repository",
            selected_repository,
        )

        # Preserve the explicit injection alias as well.
        object.__setattr__(
            self,
            "_repository",
            selected_repository,
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

    # NOTE:
    # Do NOT redefine ``repository`` as a property here.
    #
    # SandhiService already owns the canonical ``repository``
    # dataclass slot. The custom constructor initializes that
    # inherited slot directly.

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
