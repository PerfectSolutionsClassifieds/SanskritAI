from __future__ import annotations

"""
SanskritAI
==========

Morphological Dhatu Resolver

Purpose
-------
Provides the integration layer between the Morphology Kernel
and the Dhatu Kernel.

The Morphology Kernel never queries a repository directly.

Instead it delegates all dhātu retrieval to this resolver.

Architecture
------------

MorphologicalResolutionStrategy
            │
            ▼
MorphologicalDhatuResolver
            │
            ▼
DhatuRepository
            │
            ▼
DhatuCollection

Version
-------
v2.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable

from SanskritAI.domain.dhatu.dhatu import (
    Dhatu,
)

from SanskritAI.domain.dhatu.dhatu_collection import (
    DhatuCollection,
)

from SanskritAI.domain.dhatu.dhatu_repository import (
    DhatuRepository,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MorphologicalDhatuResolver(
    Immutable,
    Displayable,
):
    """
    Adapter used by the Morphology Kernel for dhātu lookup.
    """

    repository: DhatuRepository

    # ---------------------------------------------------------

    @property
    def display_name(
        self,
    ) -> str:

        return "Morphological Dhatu Resolver"

    @property
    def display_text(
        self,
    ) -> str:

        return self.display_name

    @property
    def display_description(
        self,
    ) -> str:

        return (
            "Resolves dhātus required during "
            "morphological analysis."
        )

    # ---------------------------------------------------------

    def resolve_by_root(
        self,
        root: str,
    ) -> DhatuCollection:

        return self.repository.find_by_root(
            root,
        )

    def resolve_by_identifier(
        self,
        identifier: str,
    ) -> Dhatu | None:

        return self.repository.get(
            identifier,
        )

    def search(
        self,
        query: str,
    ) -> DhatuCollection:

        return self.repository.search(
            query,
        )
