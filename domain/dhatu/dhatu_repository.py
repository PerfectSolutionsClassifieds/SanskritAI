from __future__ import annotations

"""
SanskritAI
==========

Dhatu Repository

Defines the repository abstraction for Sanskrit verbal roots.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.dhatu.dhatu_collection import DhatuCollection
from SanskritAI.domain.dhatu.dhatu_gana import DhatuGana


class DhatuRepository(
    ABC,
    Displayable,
):
    """
    Repository abstraction for Dhatu knowledge.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract repository for Sanskrit dhatu knowledge."

    @abstractmethod
    def get(self, identifier: str) -> Dhatu | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_root(self, root: str) -> DhatuCollection:
        raise NotImplementedError

    @abstractmethod
    def find_by_gana(self, gana: DhatuGana) -> DhatuCollection:
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str) -> DhatuCollection:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> DhatuCollection:
        raise NotImplementedError

    @abstractmethod
    def contains(self, identifier: str) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError
