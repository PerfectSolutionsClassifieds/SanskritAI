from __future__ import annotations

"""
SanskritAI
==========

Default Dhatu Repository

Canonical in-memory implementation of DhatuRepository.

Responsibilities
----------------
• store Dhatu value objects
• retrieve by identifier
• retrieve by root
• retrieve by DhatuGana
• perform deterministic textual search
• enumerate all Dhatus
• provide repository statistics

The repository performs no linguistic analysis.

Analysis remains the responsibility of the Dhatu
resolution pipeline:

    DhatuService
        ↓
    DhatuResolver
        ↓
    DhatuStrategy
        ↓
    DhatuAnalysis
        ↓
    DhatuResult

Version
-------
v1.0.0
"""

from typing import Iterable

from SanskritAI.core.mixins.displayable import Displayable

from SanskritAI.domain.dhatu.dhatu import Dhatu
from SanskritAI.domain.dhatu.dhatu_collection import DhatuCollection
from SanskritAI.domain.dhatu.dhatu_gana import DhatuGana
from SanskritAI.domain.dhatu.dhatu_repository import DhatuRepository


class DefaultDhatuRepository(
    DhatuRepository,
    Displayable,
):
    """
    Canonical in-memory Dhatu repository.

    Dhatus are indexed by their canonical identifier.

    Insertion order is preserved.
    """

    def __init__(
        self,
        dhatus: Iterable[Dhatu] = (),
    ) -> None:
        self._dhatus: dict[str, Dhatu] = {}

        for dhatu in dhatus:
            self.register(dhatu)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @staticmethod
    def _validate_dhatu(
        dhatu: Dhatu,
    ) -> None:
        if dhatu is None:
            raise ValueError(
                "Dhatu must not be None."
            )

        if not isinstance(dhatu, Dhatu):
            raise TypeError(
                "Expected a Dhatu instance."
            )

        if not dhatu.identifier:
            raise ValueError(
                "Dhatu identifier must not be empty."
            )

        if not dhatu.root:
            raise ValueError(
                "Dhatu root must not be empty."
            )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return "Default Dhatu Repository"

    @property
    def display_text(self) -> str:
        return self.display_name

    @property
    def display_description(self) -> str:
        return (
            "Canonical in-memory repository for Sanskrit "
            "Dhatu knowledge."
        )

    # ---------------------------------------------------------
    # Primary lookup
    # ---------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> Dhatu | None:
        """
        Retrieve a Dhatu by canonical identifier.
        """
        if not identifier:
            return None

        return self._dhatus.get(identifier)

    # ---------------------------------------------------------
    # Root lookup
    # ---------------------------------------------------------

    def find_by_root(
        self,
        root: str,
    ) -> DhatuCollection:
        """
        Retrieve all Dhatus whose root exactly matches
        the supplied Sanskrit root.

        No normalization is performed at repository level.
        """

        if not root:
            return DhatuCollection()

        matches = tuple(
            dhatu
            for dhatu in self._dhatus.values()
            if dhatu.root == root
        )

        return DhatuCollection(
            dhatus=matches,
        )

    # ---------------------------------------------------------
    # Gana lookup
    # ---------------------------------------------------------

    def find_by_gana(
        self,
        gana: DhatuGana,
    ) -> DhatuCollection:
        """
        Retrieve all Dhatus belonging to the supplied
        DhatuGana value object.
        """

        if gana is None:
            return DhatuCollection()

        matches = tuple(
            dhatu
            for dhatu in self._dhatus.values()
            if dhatu.gana == gana
        )

        return DhatuCollection(
            dhatus=matches,
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> DhatuCollection:
        """
        Perform deterministic textual repository search.

        Searches:

        • identifier
        • root
        • transliteration
        • meaning
        • notes
        • gana identifier
        • gana Sanskrit name
        • gana English name

        Search is intentionally simple.

        Linguistic normalization and semantic search belong
        to higher layers.
        """

        if not query:
            return DhatuCollection()

        normalized = query.casefold()

        matches: list[Dhatu] = []

        for dhatu in self._dhatus.values():

            searchable_fields = [
                dhatu.identifier,
                dhatu.root,
                dhatu.transliteration,
                dhatu.meaning,
                dhatu.notes,
            ]

            if dhatu.gana is not None:
                searchable_fields.extend(
                    [
                        dhatu.gana.identifier,
                        dhatu.gana.sanskrit_name,
                        dhatu.gana.english_name,
                        dhatu.gana.description,
                    ]
                )

            if any(
                normalized in field.casefold()
                for field in searchable_fields
                if field
            ):
                matches.append(dhatu)

        return DhatuCollection(
            dhatus=tuple(matches),
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(self) -> DhatuCollection:
        """
        Return all registered Dhatus in insertion order.
        """

        return DhatuCollection(
            dhatus=tuple(
                self._dhatus.values()
            ),
        )

    # ---------------------------------------------------------
    # Membership
    # ---------------------------------------------------------

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Return True when the identifier is registered.
        """

        if not identifier:
            return False

        return identifier in self._dhatus

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    @property
    def count(self) -> int:
        return len(self._dhatus)

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        dhatu: Dhatu,
    ) -> None:
        """
        Register or replace a Dhatu.

        Identifier is the canonical repository key.
        """

        self._validate_dhatu(dhatu)

        self._dhatus[
            dhatu.identifier
        ] = dhatu

    def register_many(
        self,
        dhatus: Iterable[Dhatu],
    ) -> None:
        """
        Register multiple Dhatus.
        """

        for dhatu in dhatus:
            self.register(dhatu)

    # ---------------------------------------------------------
    # Removal
    # ---------------------------------------------------------

    def remove(
        self,
        identifier: str,
    ) -> bool:
        """
        Remove a Dhatu by identifier.

        Returns
        -------
        bool
            True if removed, otherwise False.
        """

        if identifier not in self._dhatus:
            return False

        del self._dhatus[identifier]

        return True

    def clear(self) -> None:
        """
        Remove all registered Dhatus.
        """

        self._dhatus.clear()

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return self.count

    def __contains__(
        self,
        identifier: str,
    ) -> bool:
        return self.contains(identifier)

    def __str__(self) -> str:
        return self.display_text
