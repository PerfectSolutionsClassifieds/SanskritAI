from __future__ import annotations

"""
SanskritAI
==========

Context Index

Purpose
-------
Indexes CanonicalDictionarySense objects by CanonicalContext.identifier.

The index also maintains canonical-context lookup dimensions for:
• Purāṇa / corpus
• Chapter
• Śloka

Design
------
The primary ``lookup()`` operation returns dictionary senses.
The ``by_*()`` operations return CanonicalContext objects because they
represent structural navigation over the textual corpus.

Version
-------
3.0.0
"""

from dataclasses import dataclass, field
from typing import Any

from SanskritAI.acquisition.knowledge.models.canonical_context import (
    CanonicalContext,
)
from SanskritAI.acquisition.knowledge.models.canonical_dictionary_sense import (
    CanonicalDictionarySense,
)


@dataclass(slots=True)
class ContextIndex:
    # ---------------------------------------------------------
    # Primary sense index
    # ---------------------------------------------------------

    _index: dict[
        str,
        list[CanonicalDictionarySense],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    # ---------------------------------------------------------
    # Structural context indexes
    # ---------------------------------------------------------

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

    # =========================================================
    # Internal Helpers
    # =========================================================

    @staticmethod
    def _normalise(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        return str(value).strip()

    @staticmethod
    def _append_unique(
        bucket: list[CanonicalContext],
        context: CanonicalContext,
    ) -> None:
        if context not in bucket:
            bucket.append(context)

    # =========================================================
    # Registration
    # =========================================================

    def add(
        self,
        context: CanonicalContext,
        sense: CanonicalDictionarySense,
    ) -> None:
        if context is None:
            return

        identifier = self._normalise(
            getattr(context, "identifier", None),
        )

        if not identifier:
            return

        # -----------------------------------------------------
        # Primary sense index
        # -----------------------------------------------------

        bucket = self._index.setdefault(
            identifier,
            [],
        )

        if sense not in bucket:
            bucket.append(
                sense,
            )

        # -----------------------------------------------------
        # Canonical context registry
        # -----------------------------------------------------

        self._contexts[identifier] = context

        # -----------------------------------------------------
        # Purāṇa / corpus
        # -----------------------------------------------------

        purana = self._normalise(
            getattr(context, "corpus", None),
        )

        if purana:
            p_bucket = self._purana_index.setdefault(
                purana,
                [],
            )
            self._append_unique(
                p_bucket,
                context,
            )

        # -----------------------------------------------------
        # Chapter
        # -----------------------------------------------------

        chapter_identifier = self._chapter_identifier(
            context,
        )

        if chapter_identifier:
            c_bucket = self._chapter_index.setdefault(
                chapter_identifier,
                [],
            )
            self._append_unique(
                c_bucket,
                context,
            )

        # -----------------------------------------------------
        # Śloka
        # -----------------------------------------------------

        sloka_identifier = self._sloka_identifier(
            context,
        )

        if sloka_identifier:
            s_bucket = self._sloka_index.setdefault(
                sloka_identifier,
                [],
            )
            self._append_unique(
                s_bucket,
                context,
            )

    # =========================================================
    # Identifier Construction
    # =========================================================

    @classmethod
    def _chapter_identifier(
        cls,
        context: CanonicalContext,
    ) -> str:
        parts = [
            cls._normalise(getattr(context, "corpus", None)),
            cls._normalise(getattr(context, "work", None)),
            cls._normalise(getattr(context, "chapter", None)),
        ]

        if not all(parts):
            return ""

        return ":".join(parts)

    @classmethod
    def _sloka_identifier(
        cls,
        context: CanonicalContext,
    ) -> str:
        parts = [
            cls._normalise(getattr(context, "corpus", None)),
            cls._normalise(getattr(context, "work", None)),
            cls._normalise(getattr(context, "chapter", None)),
            cls._normalise(getattr(context, "verse", None)),
        ]

        if not all(parts):
            return ""

        return ":".join(parts)

    # =========================================================
    # Sense Lookup
    # =========================================================

    def lookup(
        self,
        context_identifier: str | CanonicalContext,
    ) -> tuple[
        CanonicalDictionarySense,
        ...,
    ]:
        if isinstance(
            context_identifier,
            CanonicalContext,
        ):
            identifier = self._normalise(
                getattr(context_identifier, "identifier", None),
            )
        else:
            identifier = self._normalise(
                context_identifier,
            )

        if not identifier:
            return ()

        return tuple(
            self._index.get(
                identifier,
                [],
            )
        )

    # =========================================================
    # Structural Context Lookup
    # =========================================================

    def by_purana(
        self,
        purana_name: str,
    ) -> tuple[
        CanonicalContext,
        ...,
    ]:
        key = self._normalise(
            purana_name,
        )

        return tuple(
            self._purana_index.get(
                key,
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
        key = self._normalise(
            chapter_identifier,
        )

        return tuple(
            self._chapter_index.get(
                key,
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
        key = self._normalise(
            sloka_identifier,
        )

        return tuple(
            self._sloka_index.get(
                key,
                [],
            )
        )

    # =========================================================
    # Maintenance
    # =========================================================

    def clear(
        self,
    ) -> None:
        self._index.clear()
        self._contexts.clear()
        self._purana_index.clear()
        self._chapter_index.clear()
        self._sloka_index.clear()

    # =========================================================
    # Diagnostics
    # =========================================================

    @property
    def context_count(
        self,
    ) -> int:
        return len(
            self._index,
        )

    @property
    def purana_count(
        self,
    ) -> int:
        return len(
            self._purana_index,
        )

    @property
    def chapter_count(
        self,
    ) -> int:
        return len(
            self._chapter_index,
        )

    @property
    def sloka_count(
        self,
    ) -> int:
        return len(
            self._sloka_index,
        )

    def summary(
        self,
    ) -> dict:
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
        return (
            self._normalise(
                context_identifier,
            )
            in self._index
        )

    def __len__(
        self,
    ) -> int:
        return self.context_count

    def __iter__(
        self,
    ):
        yield from sorted(
            self._index.keys(),
        )

    def __str__(
        self,
    ) -> str:
        return (
            "ContextIndex("
            f"{self.context_count} contexts)"
        )
