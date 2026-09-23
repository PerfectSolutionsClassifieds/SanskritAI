
from __future__ import annotations

"""
SanskritAI
==========

Lemma Index

Purpose
-------
Provides canonical indexing over Sanskrit lexical lemmas.

The current CanonicalLemma model uses its ``lemma`` field as the
canonical lexical identity.

Responsibilities
----------------
• Index canonical lemmas
• Retrieve lemma by canonical lemma identity
• Retrieve lemma by text
• Enumerate lemmas
• Support future reverse lookup

Version
-------
2.0.0
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

    _lemmas: dict[str, CanonicalLemma] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    _text_index: dict[str, CanonicalLemma] = field(
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

        The canonical lemma text is used as the stable lookup key.
        """

        key = lemma.lemma.strip()

        if not key:
            return

        self._lemmas.setdefault(
            key,
            lemma,
        )

        self._text_index.setdefault(
            key,
            lemma,
        )

    def build(
        self,
        lemmas: tuple[CanonicalLemma, ...],
    ) -> None:
        """
        Rebuilds the complete lemma index.
        """

        self.clear()

        for lemma in lemmas:
            self.add(lemma)

    def clear(
        self,
    ) -> None:
        """
        Clears the complete lemma index.
        """

        self._lemmas.clear()
        self._text_index.clear()

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def lookup(
        self,
        lemma_id: str,
    ) -> CanonicalLemma | None:
        """
        Looks up a lemma by its canonical identity.

        ``lemma_id`` is retained as the API parameter name for
        backward conceptual compatibility, but the current
        CanonicalLemma identity is its ``lemma`` value.
        """

        return self._lemmas.get(
            lemma_id,
        )

    def lookup_text(
        self,
        text: str,
    ) -> CanonicalLemma | None:
        """
        Looks up a lemma by its textual form.
        """

        return self._text_index.get(
            text.strip(),
        )

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(
        self,
    ) -> tuple[CanonicalLemma, ...]:
        """
        Returns all indexed lemmas sorted by lemma text.
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
        Returns canonical lemma identities.
        """

        return tuple(
            sorted(
                self._lemmas.keys(),
            )
        )

    @property
    def lemma_texts(
        self,
    ) -> tuple[str, ...]:
        """
        Returns all indexed lemma texts.
        """

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
            "lemmas": len(self),
            "lemma_ids": len(self.lemma_ids),
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

        
