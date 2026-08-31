from __future__ import annotations

"""
SanskritAI
==========

Lemma Index

Purpose
-------
Provides canonical indexing over Sanskrit lexical lemmas.

Unlike the HeadwordIndex, which indexes dictionary headwords exactly
as they appear, the LemmaIndex groups dictionary entries that share
the same normalized lexical identity.

Responsibilities
----------------
• Index lemmas
• Retrieve lemma by identifier
• Retrieve lemma by text
• Enumerate lemmas
• Support future reverse lookup

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
class LemmaIndex:
    """
    Canonical searchable lemma index.

    Two lookup maps are maintained:

    ``_lemmas``
        Stable identifier -> CanonicalLemma

    ``_text_index``
        Lemma text -> CanonicalLemma
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
    # Internal Key Resolution
    # ---------------------------------------------------------

    @staticmethod
    def _lemma_id(lemma: CanonicalLemma) -> str:
        """
        Resolve the stable lemma identifier.

        The canonical model exposes ``lemma_id`` directly.

        The fallback keeps the index compatible with lightweight
        test doubles exposing only ``lemma`` or ``text``.
        """

        value = getattr(lemma, "lemma_id", None)

        if value is None:
            value = getattr(lemma, "lemma", None)

        if value is None:
            value = getattr(lemma, "text", None)

        if value is None:
            raise AttributeError(
                "Lemma object must provide "
                "'lemma_id', 'lemma', or 'text'."
            )

        value = str(value).strip()

        if not value:
            raise ValueError(
                "Lemma identifier cannot be empty."
            )

        return value

    @staticmethod
    def _lemma_text(lemma: CanonicalLemma) -> str:
        """
        Resolve the canonical lemma text.

        The canonical model exposes ``text`` as an accessor.
        """

        value = getattr(lemma, "text", None)

        if value is None:
            value = getattr(lemma, "lemma", None)

        if value is None:
            raise AttributeError(
                "Lemma object must provide "
                "'text' or 'lemma'."
            )

        value = str(value).strip()

        if not value:
            raise ValueError(
                "Lemma text cannot be empty."
            )

        return value

    # ---------------------------------------------------------
    # Index Construction
    # ---------------------------------------------------------

    def add(
        self,
        lemma: CanonicalLemma,
    ) -> None:
        """
        Adds one canonical lemma.

        Duplicate identifiers preserve the first registered lemma.

        Duplicate textual forms also preserve the first registered
        lemma.
        """

        lemma_id = self._lemma_id(lemma)
        text = self._lemma_text(lemma)

        self._lemmas.setdefault(
            lemma_id,
            lemma,
        )

        self._text_index.setdefault(
            text,
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

    def clear(self) -> None:
        """
        Removes all indexed lemmas.
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
        Looks up a lemma by stable identifier.
        """

        return self._lemmas.get(lemma_id)

    def lookup_text(
        self,
        text: str,
    ) -> CanonicalLemma | None:
        """
        Looks up a lemma by canonical text.
        """

        return self._text_index.get(text)

    # ---------------------------------------------------------
    # Enumeration
    # ---------------------------------------------------------

    def all(
        self,
    ) -> tuple[CanonicalLemma, ...]:
        """
        Returns all indexed lemmas sorted by textual form.
        """

        return tuple(
            sorted(
                self._lemmas.values(),
                key=self._lemma_text,
            )
        )

    @property
    def lemma_ids(self) -> tuple[str, ...]:
        """
        Returns all lemma identifiers in sorted order.
        """

        return tuple(
            sorted(
                self._lemmas.keys(),
            )
        )

    @property
    def lemma_texts(self) -> tuple[str, ...]:
        """
        Returns all indexed lemma texts in sorted order.
        """

        return tuple(
            sorted(
                self._text_index.keys(),
            )
        )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(self) -> dict:
        return {
            "lemmas": len(self),
            "lemma_ids": len(self.lemma_ids),
        }

    # ---------------------------------------------------------
    # Python Protocol
    # ---------------------------------------------------------

    def __len__(self) -> int:
        return len(self._lemmas)

    def __iter__(self):
        yield from self.all()

    def __contains__(
        self,
        lemma_id: str,
    ) -> bool:
        return lemma_id in self._lemmas

    def __str__(self) -> str:
        return (
            "LemmaIndex("
            f"{len(self)} indexed lemmas)"
        )
