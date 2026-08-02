from __future__ import annotations

"""
SanskritAI
==========

Paninian Sūtra Index

Domain-specific indexed collection of executable
Paninian Sūtras.

Purpose
-------

Builds immutable indexes over executable sūtras.

Owns multiple indexes

    • sutra_number

    • adhyaya

    • pada

    • category

    • operation

    • behaviour

Version
-------
v1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.core.indexing.indexed_collection import (
    IndexedCollection,
)

from SanskritAI.core.indexing.immutable_index import (
    ImmutableIndex,
)

from SanskritAI.core.indexing.multi_index import (
    MultiIndex,
)

from SanskritAI.domain.panini.paninian_rule import (
    PaninianRule,
)


@dataclass(frozen=True, slots=True)
class PaninianSutraIndex(
    IndexedCollection[PaninianRule],
):
    """
    Indexed executable Paninian Sūtras.
    """

    indexes: MultiIndex = field(init=False)

    def __post_init__(self):

        object.__setattr__(
            self,
            "indexes",
            MultiIndex(
                indexes={
                    "sutra_number": ImmutableIndex.build(
                        self.items,
                        key_selector=lambda r: r.sutra_number,
                    ),
                    "adhyaya": ImmutableIndex.build(
                        self.items,
                        key_selector=lambda r: r.adhyaya,
                    ),
                    "pada": ImmutableIndex.build(
                        self.items,
                        key_selector=lambda r: r.pada,
                    ),
                    "category": ImmutableIndex.build(
                        self.items,
                        key_selector=lambda r: r.metadata.category,
                    ),
                    "operation": ImmutableIndex.build(
                        self.items,
                        key_selector=lambda r: r.metadata.operation,
                    ),
                    "behaviour": ImmutableIndex.build(
                        self.items,
                        key_selector=lambda r: r.behaviour,
                    ),
                }
            ),
        )

    # ---------------------------------------------------------
    # Canonical lookup
    # ---------------------------------------------------------

    def by_sutra_number(
        self,
        sutra_number: str,
    ) -> PaninianRule | None:

        return (
            self.indexes
            .get_index("sutra_number")
            .first(sutra_number)
        )

    def by_adhyaya(
        self,
        adhyaya: int,
    ) -> tuple[PaninianRule, ...]:

        return (
            self.indexes
            .get_index("adhyaya")
            .get(adhyaya)
        )

    def by_pada(
        self,
        pada: int,
    ) -> tuple[PaninianRule, ...]:

        return (
            self.indexes
            .get_index("pada")
            .get(pada)
        )

    def by_category(
        self,
        category,
    ) -> tuple[PaninianRule, ...]:

        return (
            self.indexes
            .get_index("category")
            .get(category)
        )

    def by_operation(
        self,
        operation,
    ) -> tuple[PaninianRule, ...]:

        return (
            self.indexes
            .get_index("operation")
            .get(operation)
        )

    def by_behaviour(
        self,
        behaviour,
    ) -> tuple[PaninianRule, ...]:

        return (
            self.indexes
            .get_index("behaviour")
            .get(behaviour)
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {
            "sutra_count": self.count,
            "indexes": self.indexes.summary(),
        }
