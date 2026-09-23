from __future__ import annotations

"""
SanskritAI
==========

Paninian Sutra Catalog

Public façade over the executable Paninian
Sūtra infrastructure.

Purpose
-------

The catalog is the primary public API for accessing
implemented Paninian Sūtras.

It orchestrates

    • discovery

    • loading

    • registration

    • lookup

while hiding the underlying implementation.

Architecture
------------

            Catalog
               │
     ┌─────────┴─────────┐
     ▼                   ▼
 Loader              Registry
     │                   │
     └─────────┬─────────┘
               ▼
        Executable Sūtras

Version
-------
v1.0.0
"""

from dataclasses import dataclass, field

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)

from SanskritAI.domain.panini.paninian_sutra_loader import (
    PaninianSutraLoader,
)

from SanskritAI.domain.panini.paninian_sutra_registry import (
    PaninianSutraRegistry,
)


@dataclass(slots=True)
class PaninianSutraCatalog:
    """
    Public façade for executable Paninian Sūtras.
    """

    registry: PaninianSutraRegistry = field(
        default_factory=PaninianSutraRegistry,
    )

    loader: PaninianSutraLoader = field(
        default_factory=PaninianSutraLoader,
    )

    _loaded: bool = False

    # ---------------------------------------------------------
    # Loading
    # ---------------------------------------------------------

    def load(
        self,
    ) -> None:
        """
        Loads every executable sūtra exactly once.
        """

        if self._loaded:
            return

        self.loader.load_all()

        self._loaded = True

    @property
    def is_loaded(
        self,
    ) -> bool:
        return self._loaded

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        sutra_number: str,
    ) -> PaninianRule:
        """
        Returns one executable sūtra instance.
        """

        self.load()

        return self.registry.create(
            sutra_number,
        )

    def contains(
        self,
        sutra_number: str,
    ) -> bool:

        self.load()

        return self.registry.contains(
            sutra_number,
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(
        self,
    ) -> tuple[PaninianRule, ...]:

        self.load()

        return self.registry.instances()

    @property
    def sutra_numbers(
        self,
    ) -> tuple[str, ...]:

        self.load()

        return self.registry.sutra_numbers

    @property
    def count(
        self,
    ) -> int:

        self.load()

        return len(
            self.registry,
        )

    # ---------------------------------------------------------
    # Iteration
    # ---------------------------------------------------------

    def __iter__(
        self,
    ):

        yield from self.all()

    def __len__(
        self,
    ) -> int:

        return self.count

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        self.load()

        return {

            "loaded": self.is_loaded,

            "sutra_count": self.count,

            "sutra_numbers": self.sutra_numbers,

        }

    def __str__(
        self,
    ) -> str:

        return (
            "PaninianSutraCatalog("
            f"{self.count} sūtras)"
        )
