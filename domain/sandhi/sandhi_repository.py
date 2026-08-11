from __future__ import annotations

"""
SanskritAI
==========

Sandhi Repository

Defines the canonical repository abstraction for Sanskrit
Sandhi knowledge.

A SandhiRepository provides access to canonical Sandhi
rules and supports lookup operations used by the
Sandhi Resolution Kernel.

The repository intentionally contains no Sandhi logic;
it only provides access to canonical knowledge.

Relationship
------------

CanonicalKnowledgeRepository
        │
        └── SandhiRepository

SandhiService
        │
        ▼
SandhiRepository

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.sandhi.sandhi_rule import SandhiRule
from SanskritAI.domain.sandhi.sandhi_rule_set import SandhiRuleSet


class SandhiRepository(
    ABC,
    Displayable,
):
    """
    Repository abstraction for canonical Sandhi knowledge.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Abstract repository for canonical Sandhi rules."
        )

    # ---------------------------------------------------------
    # Rule lookup
    # ---------------------------------------------------------

    @abstractmethod
    def get(
        self,
        identifier: str,
    ) -> SandhiRule | None:
        """
        Returns one rule by identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Returns True if rule exists.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> SandhiRuleSet:
        """
        Searches canonical Sandhi rules.
        """
        raise NotImplementedError

    @abstractmethod
    def all(
        self,
    ) -> SandhiRuleSet:
        """
        Returns the complete canonical rule set.
        """
        raise NotImplementedError

    # ---------------------------------------------------------

    @property
    @abstractmethod
    def count(
        self,
    ) -> int:
        """
        Total number of canonical Sandhi rules.
        """
        raise NotImplementedError
