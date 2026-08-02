from __future__ import annotations

"""
SanskritAI
==========

Paninian Sutra Catalog

Public façade over the executable Paninian
Sūtra infrastructure.

Architecture
------------

Filesystem
      │
      ▼
PaninianSutraLoader
      │
      ▼
Registration Decorator
      │
      ▼
PaninianSutraRegistry
      │
      ▼
PaninianSutraIndex
      │
      ▼
PaninianSutraCatalog

The Catalog is the only public entry point.
"""

from dataclasses import dataclass, field

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)

from SanskritAI.domain.panini.paninian_sutra_index import (
    PaninianSutraIndex,
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

    loader: PaninianSutraLoader = field(
        default_factory=PaninianSutraLoader,
    )

    registry: PaninianSutraRegistry = field(
        default_factory=PaninianSutraRegistry,
    )

    _index: PaninianSutraIndex | None = field(
        default=None,
        init=False,
        repr=False,
    )

    _loaded: bool = field(
        default=False,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Loading
    # ---------------------------------------------------------

    def load(
        self,
    ) -> None:
        """
        Loads all executable sūtras exactly once
        and builds the immutable index.
        """

        if self._loaded:
            return

        # Import every sutra module
        self.loader.load_all()

        # Build immutable index
        self._index = PaninianSutraIndex(
            items=self.registry.instances(),
        )

        self._loaded = True

    @property
    def is_loaded(
        self,
    ) -> bool:
        return self._loaded

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    @property
    def index(
        self,
    ) -> PaninianSutraIndex:

        self.load()

        assert self._index is not None

        return self._index

    # ---------------------------------------------------------
    # Canonical Lookup
    # ---------------------------------------------------------

    def get(
        self,
        sutra_number: str,
    ) -> PaninianRule | None:
        """
        Returns one executable sutra.
        """

        return self.index.by_sutra_number(
            sutra_number,
        )

    def by_adhyaya(
        self,
        adhyaya: int,
    ) -> tuple[PaninianRule, ...]:

        return self.index.by_adhyaya(
            adhyaya,
        )

    def by_pada(
        self,
        pada: int,
    ) -> tuple[PaninianRule, ...]:

        return self.index.by_pada(
            pada,
        )

    def by_category(
        self,
        category,
    ) -> tuple[PaninianRule, ...]:

        return self.index.by_category(
            category,
        )

    def by_operation(
        self,
        operation,
    ) -> tuple[PaninianRule, ...]:

        return self.index.by_operation(
            operation,
        )

    def by_behaviour(
        self,
        behaviour,
    ) -> tuple[PaninianRule, ...]:

        return self.index.by_behaviour(
            behaviour,
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(
        self,
    ) -> tuple[PaninianRule, ...]:

        return self.index.items

    @property
    def count(
        self,
    ) -> int:

        return len(
            self.index,
        )

    @property
    def sutra_numbers(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            sorted(
                sutra.sutra_number
                for sutra in self.index.items
            )
        )

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return self.count

    def __iter__(
        self,
    ):

        yield from self.index.items

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {
            "loaded": self.is_loaded,
            "sutra_count": self.count,
            "index": self.index.summary(),
        }

    def __str__(
        self,
    ) -> str:

        return (
            "PaninianSutraCatalog("
            f"{self.count} executable sūtras)"
        )
