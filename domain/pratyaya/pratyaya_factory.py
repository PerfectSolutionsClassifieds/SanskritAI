from __future__ import annotations

"""
SanskritAI
==========

Pratyaya Factory

Constructs immutable Pratyaya objects from declarative
PratyayaSpecification objects.

The factory contains no hard-coded affix inventory. Canonical
Pratyayas are defined separately in pratyaya_specification.py.

Hierarchy
---------

PratyayaSpecification
        │
        ▼
PratyayaFactory
        │
        ├── create_pratyaya()
        ├── create_pratyayas()
        ├── create_collection()
        └── create_default_collection()

Version
-------
v1.0.0
"""

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Iterator

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.domain.pratyaya.pratyaya_specification import (
    CANONICAL_PRATYAYA_SPECIFICATION,
    PratyayaSpecification,
)


@dataclass(frozen=True, slots=True)
class Pratyaya(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable Sanskrit Pratyaya.
    """

    identifier: str

    pratyaya: str

    transliteration: str = ""

    meaning: str = ""

    category: str = ""

    notes: str = ""

    @property
    def display_name(self) -> str:
        return self.pratyaya

    @property
    def display_text(self) -> str:
        if self.transliteration:
            return f"{self.pratyaya} ({self.transliteration})"
        return self.pratyaya

    @property
    def display_description(self) -> str:
        return self.meaning or self.notes

    @property
    def has_category(self) -> bool:
        return bool(self.category)

    @property
    def has_notes(self) -> bool:
        return bool(self.notes)

    def __str__(self) -> str:
        return self.display_text


@dataclass(frozen=True, slots=True)
class PratyayaCollection(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable collection of Pratyaya objects.
    """

    pratyayas: tuple[
        Pratyaya,
        ...
    ] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        return "Pratyaya Collection"

    @property
    def display_text(self) -> str:
        return f"{len(self.pratyayas)} Pratyayas"

    @property
    def display_description(self) -> str:
        return "Immutable collection of Sanskrit pratyayas."

    @property
    def count(self) -> int:
        return len(self.pratyayas)

    @property
    def is_empty(self) -> bool:
        return self.count == 0

    @property
    def first(self) -> Pratyaya | None:
        if self.is_empty:
            return None
        return self.pratyayas[0]

    def add(self, pratyaya: Pratyaya) -> "PratyayaCollection":
        return PratyayaCollection(
            pratyayas=self.pratyayas + (pratyaya,)
        )

    def extend(self, other: "PratyayaCollection") -> "PratyayaCollection":
        return PratyayaCollection(
            pratyayas=self.pratyayas + other.pratyayas
        )

    def get_by_identifier(self, identifier: str) -> Pratyaya | None:
        for pratyaya in self.pratyayas:
            if pratyaya.identifier == identifier:
                return pratyaya
        return None

    def __iter__(self) -> Iterator[Pratyaya]:
        return iter(self.pratyayas)

    def __len__(self) -> int:
        return len(self.pratyayas)

    def __getitem__(self, index: int) -> Pratyaya:
        return self.pratyayas[index]

    def __str__(self) -> str:
        return self.display_text


class PratyayaFactory:
    """
    Factory responsible for constructing immutable Pratyaya
    objects from declarative specifications.
    """

    @staticmethod
    def create_pratyaya(
        specification: PratyayaSpecification,
    ) -> Pratyaya:
        """
        Constructs one immutable Pratyaya.
        """
        return Pratyaya(
            identifier=specification.identifier,
            pratyaya=specification.pratyaya,
            transliteration=specification.transliteration,
            meaning=specification.meaning,
            category=specification.category,
            notes=specification.notes,
        )

    @classmethod
    def create_pratyayas(
        cls,
        specification: Iterable[PratyayaSpecification],
    ) -> tuple[Pratyaya, ...]:
        """
        Constructs immutable Pratyaya objects.
        """
        return tuple(
            cls.create_pratyaya(item)
            for item in specification
        )

    @classmethod
    def create_collection(
        cls,
        specification: Iterable[PratyayaSpecification],
    ) -> PratyayaCollection:
        """
        Constructs an immutable PratyayaCollection.
        """
        return PratyayaCollection(
            pratyayas=cls.create_pratyayas(specification)
        )

    @classmethod
    def create_default_collection(
        cls,
    ) -> PratyayaCollection:
        """
        Constructs the canonical Pratyaya collection.
        """
        return cls.create_collection(
            CANONICAL_PRATYAYA_SPECIFICATION
        )
