from __future__ import annotations

"""
SanskritAI
==========

Morphological Repository

Canonical repository abstraction for Sanskrit morphological
knowledge.

This repository serves as the authoritative source for
grammatical categories and morphology rules.

It intentionally contains NO analysis logic.

Responsibilities
----------------

• provide canonical grammatical categories

• provide morphology rule sets

• provide nominal rule lookup

• provide verbal rule lookup

• provide category lookup

• provide morphology metadata

Relationship
------------

CanonicalKnowledgeRepository
            │
            ▼
MorphologicalRepository
            │
            ├── MorphologicalRuleSet
            ├── MorphologicalRule
            ├── GrammaticalCategory
            ├── NominalCategory
            ├── VerbalCategory
            └── AvyayaCategory

Version
-------
v2.0.0
"""

from abc import ABC
from abc import abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.morphology.grammatical_category import (
    GrammaticalCategory,
)

from SanskritAI.domain.morphology.grammatical_category_collection import (
    GrammaticalCategoryCollection,
)

from SanskritAI.domain.morphology.morphological_rule import (
    MorphologicalRule,
)

from SanskritAI.domain.morphology.morphological_rule_set import (
    MorphologicalRuleSet,
)


class MorphologicalRepository(
    ABC,
    Displayable,
):
    """
    Canonical repository for morphology knowledge.
    """

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical repository for Sanskrit morphology."
        )

    # ---------------------------------------------------------
    # Category Lookup
    # ---------------------------------------------------------

    @abstractmethod
    def get_category(
        self,
        identifier: str,
    ) -> GrammaticalCategory | None:
        """
        Returns one grammatical category.
        """
        raise NotImplementedError

    @abstractmethod
    def categories(
        self,
    ) -> GrammaticalCategoryCollection:
        """
        Returns every grammatical category.
        """
        raise NotImplementedError

    @abstractmethod
    def contains_category(
        self,
        identifier: str,
    ) -> bool:
        raise NotImplementedError

    # ---------------------------------------------------------
    # Rule Lookup
    # ---------------------------------------------------------

    @abstractmethod
    def get_rule(
        self,
        identifier: str,
    ) -> MorphologicalRule | None:
        """
        Returns one morphology rule.
        """
        raise NotImplementedError

    @abstractmethod
    def rules(
        self,
    ) -> MorphologicalRuleSet:
        """
        Returns the canonical morphology rule set.
        """
        raise NotImplementedError

    @abstractmethod
    def nominal_rules(
        self,
    ) -> MorphologicalRuleSet:
        """
        Returns nominal morphology rules.
        """
        raise NotImplementedError

    @abstractmethod
    def verbal_rules(
        self,
    ) -> MorphologicalRuleSet:
        """
        Returns verbal morphology rules.
        """
        raise NotImplementedError

    @abstractmethod
    def indeclinable_rules(
        self,
    ) -> MorphologicalRuleSet:
        """
        Returns indeclinable morphology rules.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    @abstractmethod
    def category_count(
        self,
    ) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def rule_count(
        self,
    ) -> int:
        raise NotImplementedError
