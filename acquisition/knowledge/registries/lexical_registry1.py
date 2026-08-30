from __future__ import annotations

"""
SanskritAI
==========

Lexical Registry

Purpose
-------
Canonical in-memory registry of all CanonicalLexicon
objects loaded into the Canonical Knowledge Repository.

This registry is intentionally unaware of acquisition
pipelines, parsers, transformers or source-specific
implementations.

Architecture
------------

Acquisition Pipelines
        │
        ▼
CanonicalLexicon
        │
        ▼
LexicalRegistry
        │
        ▼
CanonicalKnowledgeRepository

Responsibilities
----------------

• Register canonical lexicons

• Retrieve canonical lexicons

• Enumerate lexicons

• Prevent duplicate registrations

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_lexicon import (
    CanonicalLexicon,
)


@dataclass(slots=True)
class LexicalRegistry:
    """
    Registry of CanonicalLexicon objects.
    """

    _lexicons: dict[
        str,
        CanonicalLexicon,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        lexicon: CanonicalLexicon,
    ) -> None:
        """
        Registers one canonical lexicon.

        Duplicate identifiers are ignored.
        """

        if lexicon.lexicon_id in self._lexicons:
            return

        self._lexicons[
            lexicon.lexicon_id
        ] = lexicon

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def lookup(
        self,
        lexicon_id: str,
    ) -> CanonicalLexicon | None:

        return self._lexicons.get(
            lexicon_id,
        )

    def lookup_by_name(
        self,
        name: str,
    ) -> CanonicalLexicon | None:

        for lexicon in self._lexicons.values():

            if lexicon.name == name:

                return lexicon

        return None

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(
        self,
    ) -> tuple[
        CanonicalLexicon,
        ...,
    ]:

        return tuple(
            sorted(
                self._lexicons.values(),
                key=lambda x: x.name,
            )
        )

    @property
    def lexicon_ids(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            sorted(
                self._lexicons.keys(),
            )
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "lexicons": len(
                self,
            ),

            "ids": self.lexicon_ids,

        }

    # ---------------------------------------------------------
    # Python protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._lexicons,
        )

    def __iter__(
        self,
    ):

        yield from self.all()

    def __contains__(
        self,
        lexicon_id: str,
    ) -> bool:

        return (
            lexicon_id
            in self._lexicons
        )

    def __str__(
        self,
    ) -> str:

        return (

            "LexicalRegistry("

            f"{len(self)} lexicons)"

        )
