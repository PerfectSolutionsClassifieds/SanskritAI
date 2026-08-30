
from __future__ import annotations

"""
SanskritAI
==========

Lemma Registry

Purpose
-------
Canonical in-memory registry of all CanonicalLemma objects
loaded into the Canonical Knowledge Repository.

Responsibilities
----------------
• Register canonical lemmas
• Retrieve canonical lemmas
• Lookup by lemma text
• Enumerate lemmas
• Prevent duplicate registrations

Version
-------
1.1.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)


@dataclass(slots=True)
class LemmaRegistry:
    """
    Registry of CanonicalLemma objects.
    """

    _lemmas: dict[str, CanonicalLemma] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        lemma: CanonicalLemma,
    ) -> None:
        """
        Register one canonical lemma.

        The canonical lemma text itself is used as the
        registry identifier.

        Duplicate registrations are ignored.
        """

        lemma_id = lemma.lemma

        if lemma_id in self._lemmas:
            return

        self._lemmas[lemma_id] = lemma

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def lookup(
        self,
        lemma_id: str,
    ) -> CanonicalLemma | None:
        """
        Lookup a lemma by its canonical lemma text.
        """

        return self._lemmas.get(
            lemma_id,
        )

    def lookup_by_text(
        self,
        text: str,
    ) -> CanonicalLemma | None:
        """
        Lookup by normalized lemma text.
        """

        return self._lemmas.get(
            text,
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(
        self,
    ) -> tuple[CanonicalLemma, ...]:
        """
        Return all registered lemmas sorted by lemma text.
        """

        return tuple(
            sorted(
                self._lemmas.values(),
                key=lambda x: x.lemma,
            )
        )

    @property
    def lemma_ids(
        self,
    ) -> tuple[str, ...]:
        """
        Return canonical lemma identifiers.
        """

        return tuple(
            sorted(
                self._lemmas.keys()
            )
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {
            "lemmas": len(self),
            "ids": self.lemma_ids,
        }

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._lemmas,
        )

    def __iter__(
        self,
    ):

        yield from self.all()

    def __contains__(
        self,
        lemma_id: str,
    ) -> bool:

        return lemma_id in self._lemmas

    def __str__(
        self,
    ) -> str:

        return (
            "LemmaRegistry("
            f"{len(self)} lemmas)"
        )
