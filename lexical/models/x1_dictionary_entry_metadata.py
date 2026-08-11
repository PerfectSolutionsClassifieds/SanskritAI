from __future__ import annotations

"""
SanskritAI
==========

Dictionary Entry Metadata

Defines the immutable metadata describing how a Lexeme
appears within a specific dictionary or lexical resource.

A DictionaryEntryMetadata represents dictionary-specific
editorial information and source location while inheriting
common lexical metadata from BaseLexicalMetadata.

Examples
--------

Amarakośa

Monier-Williams

Vācaspatyam

Śabdakalpadruma

Version
-------
v0.3.0
"""

from dataclasses import dataclass

from SanskritAI.lexical.models.base_lexical_metadata import (
    BaseLexicalMetadata,
)


@dataclass(frozen=True, slots=True)
class DictionaryEntryMetadata(
    BaseLexicalMetadata,
):
    """
    Immutable metadata describing a dictionary entry.
    """

    # ---------------------------------------------------------
    # Dictionary identification
    # ---------------------------------------------------------

    dictionary_name: str = ""

    dictionary_version: str = ""

    entry_identifier: str = ""

    # ---------------------------------------------------------
    # Dictionary headword
    # ---------------------------------------------------------

    headword: str = ""

    # ---------------------------------------------------------
    # Source location
    # ---------------------------------------------------------

    volume: str = ""

    chapter: str = ""

    section: str = ""

    page: str = ""

    entry_number: str = ""

    # ---------------------------------------------------------
    # Editorial information
    # ---------------------------------------------------------

    editor: str = ""

    publisher: str = ""

    publication_year: str = ""

    # ---------------------------------------------------------
    # Entry status
    # ---------------------------------------------------------

    is_primary: bool = False

    notes: str = ""

    # ---------------------------------------------------------
    # Convenience properties
    # ---------------------------------------------------------

    @property
    def display_title(self) -> str:
        """
        Preferred title for display.

        Falls back in the following order:

            headword
            lemma
            dictionary_name
        """

        if self.headword:
            return self.headword

        if self.lemma:
            return self.lemma

        return self.dictionary_name

    @property
    def has_dictionary(self) -> bool:
        return bool(self.dictionary_name)

    @property
    def has_headword(self) -> bool:
        return bool(self.headword)

    @property
    def has_location(self) -> bool:
        return any(
            (
                self.volume,
                self.chapter,
                self.section,
                self.page,
                self.entry_number,
            )
        )

    @property
    def citation(self) -> str:
        """
        Human-readable citation.

        Example

        Amarakośa Vol.1 p.52
        """

        parts: list[str] = []

        if self.dictionary_name:
            parts.append(self.dictionary_name)

        if self.volume:
            parts.append(f"Vol.{self.volume}")

        if self.page:
            parts.append(f"p.{self.page}")

        return " ".join(parts)
