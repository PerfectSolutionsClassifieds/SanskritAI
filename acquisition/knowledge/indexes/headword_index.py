
from __future__ import annotations

"""
SanskritAI
==========

Headword Index

Purpose
-------
Provides exact and prefix lookup over canonical Sanskrit
dictionary headwords.

The index stores references to immutable
CanonicalDictionaryEntry objects.

Responsibilities
----------------
• Index dictionary entries by headword
• Exact lookup
• Prefix lookup
• Enumerate indexed entries
• Clear and rebuild deterministically

No grammatical reasoning is performed here.
"""

from dataclasses import dataclass
from dataclasses import field

from SanskritAI.acquisition.knowledge.models.canonical_dictionary_entry import (
    CanonicalDictionaryEntry,
)


@dataclass(slots=True)
class HeadwordIndex:

    _entries: dict[
        str,
        CanonicalDictionaryEntry,
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
        entry: CanonicalDictionaryEntry,
    ) -> None:

        headword = entry.headword.strip()

        if not headword:
            return

        # Preserve first registration deterministically.
        self._entries.setdefault(
            headword,
            entry,
        )

    def build(
        self,
        entries: tuple[
            CanonicalDictionaryEntry,
            ...,
        ],
    ) -> None:

        self.clear()

        for entry in entries:
            self.add(entry)

    # =========================================================
    # Maintenance
    # =========================================================

    def clear(self) -> None:
        self._entries.clear()

    # =========================================================
    # Lookup
    # =========================================================

    def lookup(
        self,
        headword: str,
    ) -> CanonicalDictionaryEntry | None:

        return self._entries.get(
            headword.strip(),
        )

    # =========================================================
    # Prefix Search
    # =========================================================

    def prefix_search(
        self,
        prefix: str,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:

        prefix = prefix.strip()

        if not prefix:
            return ()

        return tuple(
            sorted(
                (
                    entry
                    for headword, entry
                    in self._entries.items()
                    if headword.startswith(prefix)
                ),
                key=lambda entry: entry.headword,
            )
        )

    # =========================================================
    # Enumeration
    # =========================================================

    def all_entries(
        self,
    ) -> tuple[
        CanonicalDictionaryEntry,
        ...,
    ]:

        return tuple(
            sorted(
                self._entries.values(),
                key=lambda entry: entry.headword,
            )
        )

    @property
    def headwords(self) -> tuple[str, ...]:
        return tuple(
            sorted(self._entries.keys())
        )

    # =========================================================
    # Diagnostics
    # =========================================================

    def summary(self) -> dict:
        return {
            "indexed_entries": len(self),
            "headwords": len(self.headwords),
        }

    # =========================================================
    # Python Protocol
    # =========================================================

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        yield from self.all_entries()

    def __contains__(
        self,
        headword: str,
    ) -> bool:

        return headword.strip() in self._entries

    def __str__(self) -> str:
        return (
            "HeadwordIndex("
            f"{len(self)} indexed entries)"
        )
