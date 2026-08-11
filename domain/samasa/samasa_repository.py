from __future__ import annotations

"""
SanskritAI
==========

Samasa Repository

Repository abstraction for canonical Samāsa knowledge.

Responsibilities
----------------

• retrieve Samāsa rules

• retrieve Samāsa definitions

• search Samāsa knowledge

• expose canonical rule collection

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.samasa.samasa_rule import SamasaRule
from SanskritAI.domain.samasa.samasa_rule_set import SamasaRuleSet


class SamasaRepository(
    ABC,
    Displayable,
):
    """
    Repository abstraction for Samāsa knowledge.
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
            "Abstract repository for canonical Samāsa knowledge."
        )

    @abstractmethod
    def get(
        self,
        identifier: str,
    ) -> SamasaRule | None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> SamasaRuleSet:
        raise NotImplementedError

    @abstractmethod
    def all(
        self,
    ) -> SamasaRuleSet:
        raise NotImplementedError

    @property
    @abstractmethod
    def count(
        self,
    ) -> int:
        raise NotImplementedError
