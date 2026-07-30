from __future__ import annotations

"""
SanskritAI
==========

Derivation Repository

Defines the repository abstraction for derivation patterns.

This repository can later be backed by:
- in-memory canonical patterns
- JSON files
- SQL databases
- graph databases
- editorial knowledge stores

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.derivation.derivation_pattern import DerivationPattern
from SanskritAI.domain.derivation.derivation_pattern_collection import (
    DerivationPatternCollection,
)


class DerivationRepository(
    ABC,
    Displayable,
):
    """
    Repository abstraction for derivation patterns.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract repository for derivation patterns."

    @abstractmethod
    def get(self, identifier: str) -> DerivationPattern | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_category(
        self,
        category: str,
    ) -> DerivationPatternCollection:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
    ) -> DerivationPatternCollection:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> DerivationPatternCollection:
        raise NotImplementedError

    @abstractmethod
    def contains(self, identifier: str) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError
