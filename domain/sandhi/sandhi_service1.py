from __future__ import annotations

"""
SanskritAI
==========

Sandhi Service

Service abstraction responsible for accessing canonical
Sandhi knowledge.

The service separates application logic from repository
implementation.

Relationship
------------

SandhiResolutionKernel
        │
        ▼
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

from SanskritAI.domain.sandhi.sandhi_repository import (
    SandhiRepository,
)

from SanskritAI.domain.sandhi.sandhi_rule import (
    SandhiRule,
)

from SanskritAI.domain.sandhi.sandhi_rule_set import (
    SandhiRuleSet,
)


class SandhiService(
    ABC,
    Displayable,
):
    """
    Abstract Sandhi service.
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
            "Abstract service for canonical Sandhi knowledge."
        )

    # ---------------------------------------------------------

    @property
    @abstractmethod
    def repository(
        self,
    ) -> SandhiRepository:
        """
        Underlying repository.
        """
        raise NotImplementedError

    # ---------------------------------------------------------

    @abstractmethod
    def get_rule(
        self,
        identifier: str,
    ) -> SandhiRule | None:
        """
        Returns a Sandhi rule.
        """
        raise NotImplementedError

    @abstractmethod
    def search_rules(
        self,
        query: str,
    ) -> SandhiRuleSet:
        """
        Searches canonical Sandhi rules.
        """
        raise NotImplementedError

    @abstractmethod
    def all_rules(
        self,
    ) -> SandhiRuleSet:
        """
        Returns all canonical rules.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def rule_count(
        self,
    ) -> int:
        """
        Number of available rules.
        """
        raise NotImplementedError
