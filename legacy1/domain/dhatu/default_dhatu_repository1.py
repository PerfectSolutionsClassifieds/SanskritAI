from __future__ import annotations

"""
SanskritAI
==========

Default Dhatu Repository

Provides the canonical in-memory repository implementation for
Sanskrit verbal roots.

Responsibilities
----------------

• store canonical Dhatu objects
• retrieve Dhatu objects by identifier
• retrieve Dhatu objects by root
• retrieve Dhatu objects by gana
• perform simple textual search
• expose immutable DhatuCollection results
• provide repository statistics

The repository contains NO Dhatu analysis logic.

Dhatu analysis remains the responsibility of:

    DhatuService
        ↓
    DhatuResolver
        ↓
    DhatuStrategy
        ↓
    DhatuRuleSet

This repository is intentionally small and deterministic.

It is designed to be replaced later by:

    • Dhātupāṭha repository
    • database-backed repository
    • Sanskrit lexical repository
    • external dictionary adapter

without changing the DhatuRepository contract.

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

    The repository preserves insertion order and uses Dhatu
    identifiers as its primary lookup key.
    """

    def __init__(
        self,
        dhatus: Iterable[Dhatu] = (),
    ) -> None:
        self._dhatus: dict[str, Dhatu] = {}

        for dhatu in dhatus:
            self._validate_dhatu(dhatu)
            self._dhatus[dhatu.identifier] = dhatu

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
    # Primary Lookup
    # ---------------------------------------------------------

    def get(
        self,
        identifier: str,
    ) -> Dhatu | None:
        """
        Returns a Dhatu by canonical identifier.
        """
        if not identifier:
            return None

        return self._dhatus.get(identifier)

    # ---------------------------------------------------------
    # Root Lookup
    # ---------------------------------------------------------

    def find_by_root(
        self,
        root: str,
    ) -> DhatuCollection:
        """
        Returns Dhatus whose root exactly matches the supplied
        root.

        Matching is intentionally exact and case-sensitive.
        Sanskrit lexical normalization belongs above the
        repository boundary.
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
    # Gana Lookup
    # ---------------------------------------------------------

    def find_by_gana(
        self,
        gana: DhatuGana,
    ) -> DhatuCollection:
        """
        Returns all Dhatus belonging to the supplied Gana.
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
        Performs a deterministic textual search.

        The query is matched against:

            • identifier
            • root
            • display text
            • display name

        Matching is case-insensitive for textual fields.

        This is intentionally a simple repository-level search.
        Linguistic normalization and semantic search belong to
        higher layers.
        """
        if not query:
            return DhatuCollection()

        normalized = query.casefold()

        matches = tuple(
            dhatu
            for dhatu in self._dhatus.values()
            if (
                normalized in dhatu.identifier.casefold()
                or normalized in dhatu.root.casefold()
                or normalized in dhatu.display_text.casefold()
                or normalized in dhatu.display_name.casefold()
            )
        )

        return DhatuCollection(
            dhatus=matches,
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(self) -> DhatuCollection:
        """
        Returns all registered Dhatus in insertion order.
        """
        return DhatuCollection(
            dhatus=tuple(self._dhatus.values()),
        )

    # ---------------------------------------------------------
    # Membership
    # ---------------------------------------------------------

    def contains(
        self,
        identifier: str,
    ) -> bool:
        """
        Returns True when the identifier is registered.
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
        Registers or replaces a Dhatu.

        Registration is deliberately kept separate from the
        abstract DhatuRepository retrieval contract.
        """
        self._validate_dhatu(dhatu)

        self._dhatus[dhatu.identifier] = dhatu

    def register_many(
        self,
        dhatus: Iterable[Dhatu],
    ) -> None:
        """
        Registers multiple Dhatus.
        """
        for dhatu in dhatus:
            self.register(dhatu)

    def remove(
        self,
        identifier: str,
    ) -> bool:
        """
        Removes a Dhatu by identifier.

        Returns True when a Dhatu was removed.
        """
        if identifier not in self._dhatus:
            return False

        del self._dhatus[identifier]
        return True

    def clear(self) -> None:
        """
        Removes all registered Dhatus.
        """
        self._dhatus.clear()

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
