from __future__ import annotations

"""
SanskritAI
==========

Paninian Rule Repository

Defines the canonical repository interface for Paninian rules.

The repository owns the canonical inventory of Paninian rules
and provides retrieval operations for the Paninian Rule Engine
and all downstream linguistic kernels.

Hierarchy
---------

PaninianRule
        │
        ▼
PaninianRuleCollection
        │
        ▼
PaninianRuleRepository
        │
        ▼
DefaultPaninianRuleRepository
        │
        ▼
PaninianRuleEngine

Future
------

Concrete repositories may be backed by

• Static Python definitions
• JSON
• YAML
• SQLite
• PostgreSQL
• Knowledge Graph
• RDF / OWL
• Neo4j

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.panini.paninian_rule import PaninianRule
from SanskritAI.domain.panini.paninian_rule_collection import (
    PaninianRuleCollection,
)


class PaninianRuleRepository(
    Displayable,
    ABC,
):
    """
    Canonical repository interface for Paninian rules.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Paninian Rule Repository"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Repository containing canonical "
            "Paninian grammatical rules."
        )

    # ---------------------------------------------------------
    # Required API
    # ---------------------------------------------------------

    @abstractmethod
    def all(
        self,
    ) -> PaninianRuleCollection:
        """
        Returns every canonical Paninian rule.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_identifier(
        self,
        identifier: str,
    ) -> PaninianRule | None:
        """
        Retrieves one rule by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_sutra(
        self,
        sutra_number: str,
    ) -> PaninianRule | None:
        """
        Retrieves one rule by its Aṣṭādhyāyī
        sūtra number.
        """
        raise NotImplementedError

    @abstractmethod
    def by_category(
        self,
        category: str,
    ) -> PaninianRuleCollection:
        """
        Returns all rules belonging to a category.

        Examples
        --------
        sandhi
        samasa
        dhatu
        pratyaya
        derivation
        grammar
        vakya
        semantics
        chandas
        alankara
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def enabled(
        self,
    ) -> PaninianRuleCollection:
        """
        Returns only enabled rules.
        """
        return self.all().enabled()

    def count(
        self,
    ) -> int:
        """
        Number of rules contained in the repository.
        """
        return self.all().count

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Checks whether a rule exists.
        """
        return (
            self.get_by_identifier(identifier)
            is not None
        )

    def __len__(self) -> int:
        return self.count()

    def __iter__(self):
        return iter(self.all())
