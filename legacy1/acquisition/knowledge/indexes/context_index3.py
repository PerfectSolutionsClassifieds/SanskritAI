
from __future__ import annotations

"""
SanskritAI
==========

Context Index

Purpose
-------
Indexes CanonicalDictionarySense objects by the canonical
CanonicalContext.identifier.

Typical Reader query:

    "Show all lexical senses associated with this textual context."
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


@dataclass(slots=True)
class ContextIndex:

    _index: dict[
        str,
        list[CanonicalDictionarySense],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # =========================================================
    # Registration
    # =========================================================

    def add(
        self,
        context: CanonicalContext,
        sense: CanonicalDictionarySense,
    ) -> None:

        identifier = context.identifier.strip()

        if not identifier:
            return

        bucket = self._index.setdefault(
            identifier,
            [],
        )

        bucket.append(sense)

    # =========================================================
    # Lookup
    # =========================================================

    def lookup(
        self,
        context_identifier: str,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:

        return tuple(
            self._index.get(
                context_identifier.strip(),
                [],
            )
        )

    # =========================================================
    # Maintenance
    # =========================================================

    def clear(self) -> None:
        self._index.clear()

    # =========================================================
    # Diagnostics
    # =========================================================

    @property
    def context_count(self) -> int:
        return len(self._index)

    def summary(self) -> dict:
        return {
            "contexts": self.context_count,
        }

    # =========================================================
    # Python Protocol
    # =========================================================

    def __contains__(
        self,
        context_identifier: str,
    ) -> bool:

        return context_identifier.strip() in self._index

    def __len__(self) -> int:
        return self.context_count

    def __iter__(self):
        yield from sorted(self._index.keys())

    def __str__(self) -> str:
        return (
            "ContextIndex("
            f"{self.context_count} contexts)"
        )
