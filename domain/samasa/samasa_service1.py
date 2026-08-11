from __future__ import annotations

"""
SanskritAI
==========

Samāsa Service

Application service for canonical Samāsa knowledge.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.samasa.samasa_repository import (
    SamasaRepository,
)

from SanskritAI.domain.samasa.samasa_rule import SamasaRule
from SanskritAI.domain.samasa.samasa_rule_set import SamasaRuleSet


class SamasaService(
    ABC,
    Displayable,
):
    """
    Service abstraction for Samāsa knowledge.
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
            "Application service for canonical Samāsa knowledge."
        )

    @property
    @abstractmethod
    def repository(
        self,
    ) -> SamasaRepository:
        raise NotImplementedError

    @abstractmethod
    def get_rule(
        self,
        identifier: str,
    ) -> SamasaRule | None:
        raise NotImplementedError

    @abstractmethod
    def search_rules(
        self,
        query: str,
    ) -> SamasaRuleSet:
        raise NotImplementedError

    @abstractmethod
    def all_rules(
        self,
    ) -> SamasaRuleSet:
        raise NotImplementedError

    @property
    @abstractmethod
    def rule_count(
        self,
    ) -> int:
        raise NotImplementedError
