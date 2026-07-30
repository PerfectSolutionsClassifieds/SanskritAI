from __future__ import annotations

"""
SanskritAI
==========

Default Paninian Rule Repository

Provides the canonical in-memory repository for Paninian rules.

This repository is intentionally lightweight. It serves as the
bootstrap repository used by the Paninian Rule Engine until the
complete Aṣṭādhyāyī rule corpus is implemented.

Future versions will gradually expand this repository to contain

    • Entire Aṣṭādhyāyī
    • Rule metadata
    • Rule precedence
    • Dependencies
    • Mahābhāṣya references
    • Kāśikā references
    • Siddhānta Kaumudī references
    • Knowledge Graph links

Version
-------
v1.0.0
"""

from SanskritAI.domain.panini.paninian_rule import PaninianRule
from SanskritAI.domain.panini.paninian_rule_collection import (
    PaninianRuleCollection,
)
from SanskritAI.domain.panini.paninian_rule_repository import (
    PaninianRuleRepository,
)


class DefaultPaninianRuleRepository(
    PaninianRuleRepository,
):
    """
    Default in-memory repository of canonical Paninian rules.
    """

    def __init__(
        self,
        rules: PaninianRuleCollection | None = None,
    ) -> None:
        self._rules = (
            rules
            if rules is not None
            else self._bootstrap_rules()
        )

    # ---------------------------------------------------------
    # Bootstrap
    # ---------------------------------------------------------

    def _bootstrap_rules(
        self,
    ) -> PaninianRuleCollection:
        """
        Creates the initial canonical repository.

        Initially empty.

        As SanskritAI evolves this will gradually contain
        the complete Paninian rule inventory.
        """
        return PaninianRuleCollection()

    # ---------------------------------------------------------
    # Repository API
    # ---------------------------------------------------------

    def all(
        self,
    ) -> PaninianRuleCollection:
        return self._rules

    def get_by_identifier(
        self,
        identifier: str,
    ) -> PaninianRule | None:
        return self._rules.get_by_identifier(
            identifier
        )

    def get_by_sutra(
        self,
        sutra_number: str,
    ) -> PaninianRule | None:
        return self._rules.get_by_sutra(
            sutra_number
        )

    def by_category(
        self,
        category: str,
    ) -> PaninianRuleCollection:
        return self._rules.find_by_category(
            category
        )

    # ---------------------------------------------------------
    # Repository Extension
    # ---------------------------------------------------------

    def with_rule(
        self,
        rule: PaninianRule,
    ) -> "DefaultPaninianRuleRepository":
        """
        Returns a new repository containing one additional
        canonical rule.
        """
        return DefaultPaninianRuleRepository(
            self._rules.add(rule)
        )

    def with_rules(
        self,
        rules: PaninianRuleCollection,
    ) -> "DefaultPaninianRuleRepository":
        """
        Returns a new repository containing all supplied
        canonical rules.
        """
        return DefaultPaninianRuleRepository(
            self._rules.extend(rules)
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def rule_count(
        self,
    ) -> int:
        return self._rules.count

    @property
    def is_empty(
        self,
    ) -> bool:
        return self._rules.is_empty

    @property
    def is_not_empty(
        self,
    ) -> bool:
        return not self.is_empty
