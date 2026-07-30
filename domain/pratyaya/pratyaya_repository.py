from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Repository

Defines the repository abstraction for Sanskrit Pratyayas.

This mirrors the Dhatu repository pattern and allows the
Pratyaya Kernel to scale from a canonical bootstrap collection
to richer dictionary/repository backends later.

Version
-------
v1.0.0
"""

from abc import ABC, abstractmethod

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.domain.pratyaya.pratyaya_factory import (
    Pratyaya,
    PratyayaCollection,
)


class PratyayaRepository(
    ABC,
    Displayable,
):
    """
    Repository abstraction for Pratyaya knowledge.
    """

    @property
    def display_name(self) -> str:
        return self.__class__.__name__

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Abstract repository for Sanskrit pratyaya knowledge."

    @abstractmethod
    def get(self, identifier: str) -> Pratyaya | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_category(self, category: str) -> PratyayaCollection:
        raise NotImplementedError

    @abstractmethod
    def find_by_surface(self, surface: str) -> PratyayaCollection:
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str) -> PratyayaCollection:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> PratyayaCollection:
        raise NotImplementedError

    @abstractmethod
    def contains(self, identifier: str) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError
