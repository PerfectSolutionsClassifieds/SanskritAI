from __future__ import annotations

"""
SanskritAI
==========

Dhatu Factory

Constructs immutable Dhatu objects and Dhatu collections from
declarative DhatuSpecification objects.

The factory contains no hard-coded lexical logic.

All canonical Dhatus are defined inside
dhatu_specification.py.

Hierarchy
---------

DhatuSpecification
        │
        ▼
DhatuFactory
        │
        ├── create_dhatu()
        ├── create_dhatus()
        ├── create_collection()
        └── create_default_collection()

Version
-------
v1.0.0
"""

from collections.abc import Iterable

from SanskritAI.domain.dhatu.dhatu import (
    Dhatu,
)

from SanskritAI.domain.dhatu.dhatu_collection import (
    DhatuCollection,
)

from SanskritAI.domain.dhatu.dhatu_specification import (
    CANONICAL_DHATU_SPECIFICATION,
    DhatuSpecification,
)


class DhatuFactory:
    """
    Factory responsible for constructing immutable Dhatu
    objects from declarative specifications.
    """

    # ---------------------------------------------------------
    # Individual Dhatu
    # ---------------------------------------------------------

    @staticmethod
    def create_dhatu(
        specification: DhatuSpecification,
    ) -> Dhatu:
        """
        Constructs one immutable Dhatu.
        """

        return Dhatu(

            identifier=specification.identifier,

            root=specification.root,

            transliteration=specification.transliteration,

            meaning=specification.meaning,

            gana=specification.gana,

            class_number=specification.class_number,

            notes=specification.notes,

        )

    # ---------------------------------------------------------
    # Multiple Dhatus
    # ---------------------------------------------------------

    @classmethod
    def create_dhatus(
        cls,
        specification: Iterable[
            DhatuSpecification
        ],
    ) -> tuple[
        Dhatu,
        ...
    ]:
        """
        Constructs immutable Dhatu objects.
        """

        return tuple(

            cls.create_dhatu(item)

            for item in specification

        )

    # ---------------------------------------------------------
    # Collection
    # ---------------------------------------------------------

    @classmethod
    def create_collection(
        cls,
        specification: Iterable[
            DhatuSpecification
        ],
    ) -> DhatuCollection:
        """
        Constructs an immutable DhatuCollection.
        """

        return DhatuCollection(

            dhatus=cls.create_dhatus(
                specification
            )

        )

    # ---------------------------------------------------------
    # Canonical Collection
    # ---------------------------------------------------------

    @classmethod
    def create_default_collection(
        cls,
    ) -> DhatuCollection:
        """
        Constructs the canonical Dhatu collection.
        """

        return cls.create_collection(

            CANONICAL_DHATU_SPECIFICATION

        )
