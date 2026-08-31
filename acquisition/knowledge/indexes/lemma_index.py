
from __future__ import annotations

"""
SanskritAI
==========

Lemma Index

Purpose
-------
Indexes immutable CanonicalLemma objects by:

    1. Stable lemma identifier
    2. Canonical lemma text

The current canonical identity model uses the lemma text
as the stable identifier.
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_lemma import (
    CanonicalLemma,
)


@dataclass(slots=True)
class LemmaIndex:

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

    # =========================================================
    # Key Resolution
    # =========================================================

    @staticmethod
    def _lemma_id(
        lemma: CanonicalLemma,
    ) -> str:

        value = getattr(
            lemma,
            "lemma_id",
            None,
        )

        if value is None:
            value = getattr(
                lemma,
                "lemma",
                None,
            )

        if value is None:
            value = getattr(
                lemma,
                "text",
                None,
            )

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
    def _lemma_text(
        lemma: CanonicalLemma,
    ) -> str:

        value = getattr(
            lemma,
            "text",
            None,
        )

        if value is None:
            value = getattr(
                lemma,
                "lemma",
                None,
            )

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

    # =========================================================
    # Registration
    # =========================================================

    def add(
        self,
        lemma: CanonicalLemma,
    ) -> None:

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
        lemmas: tuple[
            CanonicalLemma,
            ...,
        ],
    ) -> None:

        self.clear()

        for lemma in lemmas:
            self.add(lemma)

    # =========================================================
    # Maintenance
    # =========================================================

    def clear(self) -> None:
        self._lemmas.clear()
        self._text_index.clear()

    # =========================================================
    # Lookup
    # =========================================================

    def lookup(
        self,
        lemma_id: str,
    ) -> CanonicalLemma | None:

        return self._lemmas.get(
            lemma_id.strip(),
        )

    def lookup_text(
        self,
        text: str,
    ) -> CanonicalLemma | None:

        return self._text_index.get(
            text.strip(),
        )

    # =========================================================
    # Enumeration
    # =========================================================

    def all(
        self,
    ) -> tuple[CanonicalLemma, ...]:

        return tuple(
            sorted(
                self._lemmas.values(),
                key=self._lemma_text,
            )
        )

    @property
    def lemma_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(self._lemmas.keys())
        )

    @property
    def lemma_texts(self) -> tuple[str, ...]:
        return tuple(
            sorted(self._text_index.keys())
        )

    # =========================================================
    # Diagnostics
    # =========================================================

    def summary(self) -> dict:
        return {
            "lemmas": len(self),
            "lemma_ids": len(self.lemma_ids),
        }

    # =========================================================
    # Python Protocol
    # =========================================================

    def __len__(self) -> int:
        return len(self._lemmas)

    def __iter__(self):
        yield from self.all()

    def __contains__(
        self,
        lemma_id: str,
    ) -> bool:

        return lemma_id.strip() in self._lemmas

    def __str__(self) -> str:
        return (
            "LemmaIndex("
            f"{len(self)} indexed lemmas)"
        )
