from __future__ import annotations

"""
SanskritAI
==========

Context Index

Purpose
-------
Indexes contextual dictionary senses across the Canonical
Knowledge Repository.

Unlike HeadwordIndex and LemmaIndex, which organize lexical
identity, ContextIndex organizes semantic interpretation.

This is the core component enabling SanskritAI's
context-aware reader.

Example
-------

Word

    शिव

may produce different contextual meanings in

    • Śiva Purāṇa
    • Liṅga Purāṇa
    • Mahābhārata
    • Bhagavad Gītā

ContextIndex makes those distinctions searchable.

Architecture
------------

CanonicalKnowledgeRepository
            │
            ▼
        ContextIndex
            │
            ▼
CanonicalDictionarySense
            │
            ▼
CanonicalContext

Responsibilities
----------------

• Index canonical contexts

• Lookup by context identifier

• Retrieve contexts belonging to a Purāṇa

• Retrieve contexts belonging to a chapter

• Retrieve contexts belonging to a śloka

• Prepare for contextual semantic lookup

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)


@dataclass(slots=True)
class ContextIndex:
    """
    Canonical searchable context index.
    """

    _contexts: dict[
        str,
        CanonicalContext,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    _purana_index: dict[
        str,
        list[CanonicalContext],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    _chapter_index: dict[
        str,
        list[CanonicalContext],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    _sloka_index: dict[
        str,
        list[CanonicalContext],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Index Construction
    # ---------------------------------------------------------

    def add(
        self,
        context: CanonicalContext,
    ) -> None:
        """
        Adds one canonical context.
        """

        self._contexts.setdefault(
            context.context_id,
            context,
        )

        self._purana_index.setdefault(
            context.purana_name,
            [],
        ).append(
            context,
        )

        self._chapter_index.setdefault(
            context.chapter_identifier,
            [],
        ).append(
            context,
        )

        self._sloka_index.setdefault(
            context.sloka_identifier,
            [],
        ).append(
            context,
        )

    def build(
        self,
        contexts: tuple[
            CanonicalContext,
            ...,
        ],
    ) -> None:

        self.clear()

        for context in contexts:

            self.add(
                context,
            )

    def clear(
        self,
    ) -> None:

        self._contexts.clear()

        self._purana_index.clear()

        self._chapter_index.clear()

        self._sloka_index.clear()

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def lookup(
        self,
        context_id: str,
    ) -> CanonicalContext | None:

        return self._contexts.get(
            context_id,
        )

    def by_purana(
        self,
        purana_name: str,
    ) -> tuple[
        CanonicalContext,
        ...,
    ]:

        return tuple(

            self._purana_index.get(
                purana_name,
                [],
            )

        )

    def by_chapter(
        self,
        chapter_identifier: str,
    ) -> tuple[
        CanonicalContext,
        ...,
    ]:

        return tuple(

            self._chapter_index.get(
                chapter_identifier,
                [],
            )

        )

    def by_sloka(
        self,
        sloka_identifier: str,
    ) -> tuple[
        CanonicalContext,
        ...,
    ]:

        return tuple(

            self._sloka_index.get(
                sloka_identifier,
                [],
            )

        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(
        self,
    ) -> tuple[
        CanonicalContext,
        ...,
    ]:

        return tuple(

            sorted(

                self._contexts.values(),

                key=lambda x: x.context_id,

            )

        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "contexts": len(self),

            "puranas": len(
                self._purana_index,
            ),

            "chapters": len(
                self._chapter_index,
            ),

            "slokas": len(
                self._sloka_index,
            ),

        }

    # ---------------------------------------------------------
    # Python Protocol
    # ---------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._contexts,
        )

    def __iter__(
        self,
    ):

        yield from self.all()

    def __contains__(
        self,
        context_id: str,
    ) -> bool:

        return context_id in self._contexts

    def __str__(
        self,
    ) -> str:

        return (

            "ContextIndex("

            f"{len(self)} contexts)"

        )
