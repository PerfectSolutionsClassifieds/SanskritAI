from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Collection

Defines the immutable collection used to manage canonical
Paninian rules.

The collection is intentionally generic so that rules from
every linguistic kernel may coexist inside one repository.

Hierarchy
---------

PaninianRule
        │
        ▼
PaninianRuleCollection
        │
        ▼
PaninianRuleSet
        │
        ▼
PaninianRuleEngine

Future
------

The collection will eventually support

• Rule dependency graphs

• Rule precedence

• Rule conflict resolution

• Sūtra navigation

• Knowledge Graph integration

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field
from typing import Iterable

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.panini.paninian_rule import PaninianRule


@dataclass(frozen=True, slots=True)
class PaninianRuleCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of Paninian rules.
    """

    rules: tuple[
        PaninianRule,
        ...
    ] = field(default_factory=tuple)

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Rule Collection"

    @property
    def display_text(self) -> str:
        return (
            f"{self.display_name}"
            f" ({self.count} rules)"
        )

    @property
    def display_description(self) -> str:
        return (
            "Immutable collection of canonical "
            "Paninian grammatical rules."
        )

    # ---------------------------------------------------------
    # Basic Properties
    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        return len(self.rules)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def is_not_empty(self) -> bool:
        return not self.is_empty

    @property
    def first(self) -> PaninianRule | None:
        if self.is_empty:
            return None
        return self.rules[0]

    @property
    def last(self) -> PaninianRule | None:
        if self.is_empty:
            return None
        return self.rules[-1]

    @property
    def identifiers(self) -> tuple[str, ...]:
        return tuple(
            rule.identifier
            for rule in self.rules
        )

    # ---------------------------------------------------------
    # Collection Operations
    # ---------------------------------------------------------

    def add(
        self,
        rule: PaninianRule,
    ) -> "PaninianRuleCollection":
        """
        Returns a new collection with the rule appended.

        Existing identifiers are replaced.
        """
        return self.remove_by_identifier(
            rule.identifier
        ).extend((rule,))

    def extend(
        self,
        rules: Iterable[PaninianRule],
    ) -> "PaninianRuleCollection":
        return PaninianRuleCollection(
            self.rules + tuple(rules)
        )

    def sorted(
        self,
    ) -> "PaninianRuleCollection":
        """
        Returns rules ordered by priority.
        Lower priority value executes first.
        """
        return PaninianRuleCollection(
            tuple(sorted(self.rules))
        )

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get_by_identifier(
        self,
        identifier: str,
    ) -> PaninianRule | None:
        for rule in self.rules:
            if rule.identifier == identifier:
                return rule
        return None

    def get_by_sutra(
        self,
        sutra_number: str,
    ) -> PaninianRule | None:
        for rule in self.rules:
            if rule.sutra_number == sutra_number:
                return rule
        return None

    def find_by_category(
        self,
        category: str,
    ) -> "PaninianRuleCollection":
        return PaninianRuleCollection(
            tuple(
                rule
                for rule in self.rules
                if rule.category.lower()
                == category.lower()
            )
        )

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    def enabled(
        self,
    ) -> "PaninianRuleCollection":
        return PaninianRuleCollection(
            tuple(
                rule
                for rule in self.rules
                if rule.enabled
            )
        )

    def disabled(
        self,
    ) -> "PaninianRuleCollection":
        return PaninianRuleCollection(
            tuple(
                rule
                for rule in self.rules
                if not rule.enabled
            )
        )

    # ---------------------------------------------------------
    # Removal
    # ---------------------------------------------------------

    def remove_by_identifier(
        self,
        identifier: str,
    ) -> "PaninianRuleCollection":
        return PaninianRuleCollection(
            tuple(
                rule
                for rule in self.rules
                if rule.identifier != identifier
            )
        )

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(self):
        return iter(self.rules)

    def __len__(self) -> int:
        return self.count

    def __contains__(
        self,
        identifier: str,
    ) -> bool:
        return (
            self.get_by_identifier(identifier)
            is not None
        )

    def __getitem__(
        self,
        index: int,
    ) -> PaninianRule:
        return self.rules[index]

    def __str__(self) -> str:
        return self.display_text
