from __future__ import annotations

"""
SanskritAI
==========

Lemma Index

Purpose
-------
Provides canonical indexing over Sanskrit lexical lemmas.

Unlike the HeadwordIndex, which indexes dictionary
headwords exactly as they appear, the LemmaIndex groups
all dictionary entries that share the same normalized
lexical identity (lemma).

Examples
--------

Headwords

    गच्छति
    अगमत्
    गमनम्

may all resolve to the lemma

    गम्

Architecture
------------

CanonicalKnowledgeRepository
            │
            ▼
        LemmaIndex
            │
            ▼
      CanonicalLemma
            │
            ▼
CanonicalDictionaryEntry

Responsibilities
----------------

• Index lemmas

• Retrieve lemma by identifier

• Retrieve lemma by text

• Enumerate lemmas

• Support future reverse lookup

Version
-------
1.0.0
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)


@dataclass(slots=True)
class LemmaIndex:
    """
    Canonical searchable lemma index.
    """

    _lemmas: dict[
        str,
        CanonicalLemma,
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    _text_index: dict[
        str,
        CanonicalLemma,
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
        lemma: CanonicalLemma,
    ) -> None:
        """
        Adds one canonical lemma.
        """

        self._lemmas.setdefault(
            lemma.lemma_id,
            lemma,
        )

        self._text_index.setdefault(
            lemma.text,
            lemma,
        )

    def build(
        self,
        lemmas: tuple[
            CanonicalLemma,
            ...,
        ],
    ) -> None:
        """
        Rebuilds the complete lemma index.
        """

        self.clear()

        for lemma in lemmas:

            self.add(
                lemma,
            )

    def clear(
        self,
    ) -> None:

        self._lemmas.clear()

        self._text_index.clear()

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def lookup(
        self,
        lemma_id: str,
    ) -> CanonicalLemma | None:

        return self._lemmas.get(
            lemma_id,
        )

    def lookup_text(
        self,
        text: str,
    ) -> CanonicalLemma | None:

        return self._text_index.get(
            text,
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(
        self,
    ) -> tuple[
        CanonicalLemma,
        ...,
    ]:

        return tuple(

            sorted(

                self._lemmas.values(),

                key=lambda x: x.text,

            )

        )

    @property
    def lemma_ids(
        self,
    ) -> tuple[
        str,
        ...,
    ]:

        return tuple(

            sorted(

                self._lemmas.keys(),

            )

        )

    @property
    def lemma_texts(
        self,
    ) -> tuple[
        str,
        ...,
    ]:

        return tuple(

            sorted(

                self._text_index.keys(),

            )

        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {

            "lemmas": len(
                self,
            ),

            "lemma_ids": len(
                self.lemma_ids,
            ),

        }

    # ---------------------------------------------------------
    # Python Protocol
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

            "LemmaIndex("

            f"{len(self)} indexed lemmas)"

        )
