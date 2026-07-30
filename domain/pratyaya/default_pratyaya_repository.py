from __future__ import annotations

"""
SanskritAI
==========

Default Pratyaya Repository

Canonical in-memory repository for Sanskrit Pratyayas.

This updated repository provides a broader canonical backing
store so the Pratyaya Kernel can rank and normalize affixes
more effectively.

Version
-------
v1.1.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.pratyaya.pratyaya_factory import (
    Pratyaya,
    PratyayaCollection,
    PratyayaFactory,
)
from SanskritAI.domain.pratyaya.pratyaya_repository import (
    PratyayaRepository,
)


@dataclass(frozen=True, slots=True)
class DefaultPratyayaRepository(
    PratyayaRepository,
):
    """
    Canonical in-memory repository of Pratyayas.
    """

    collection: PratyayaCollection = field(
        default_factory=PratyayaFactory.create_default_collection,
    )

    @property
    def display_name(self) -> str:
        return "Default Pratyaya Repository"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return "Canonical in-memory repository of Sanskrit pratyayas."

    def get(self, identifier: str) -> Pratyaya | None:
        return self.collection.get_by_identifier(identifier)

    def find_by_category(self, category: str) -> PratyayaCollection:
        needle = category.strip().lower()
        if not needle:
            return PratyayaCollection()

        return PratyayaCollection(
            pratyayas=tuple(
                item
                for item in self.collection
                if item.category.lower() == needle
            )
        )

    def find_by_surface(self, surface: str) -> PratyayaCollection:
        needle = surface.strip()
        if not needle:
            return PratyayaCollection()

        return PratyayaCollection(
            pratyayas=tuple(
                item
                for item in self.collection
                if needle == item.pratyaya
                or needle.endswith(item.pratyaya)
                or item.pratyaya in needle
            )
        )

    def search(self, query: str) -> PratyayaCollection:
        needle = query.strip().lower()
        if not needle:
            return self.collection

        return PratyayaCollection(
            pratyayas=tuple(
                item
                for item in self.collection
                if needle in item.identifier.lower()
                or needle in item.pratyaya.lower()
                or needle in item.transliteration.lower()
                or needle in item.meaning.lower()
                or needle in item.category.lower()
                or needle in item.notes.lower()
            )
        )

    def all(self) -> PratyayaCollection:
        return self.collection

    def contains(self, identifier: str) -> bool:
        return self.get(identifier) is not None

    @property
    def count(self) -> int:
        return self.collection.count
