from __future__ import annotations

"""
SanskritAI
==========

Dictionary Entry

Represents a lexical entry from a specific dictionary.

A DictionaryEntry describes how a Lexeme appears within a
particular lexical source (e.g. Amarakośa,
Monier-Williams, Apte, Vācaspatyam, Śabdakalpadruma).

Hierarchy
---------

Lexeme
    │
    ├── LexicalSource
    │
    └── LexicalRecord
            │
            └── DictionaryEntry

Dictionary senses are modeled separately by
DictionarySense.

Version
-------
v0.4.0
"""

from SanskritAI.lexical.models.dictionary_entry_metadata import (
    DictionaryEntryMetadata,
)
from SanskritAI.lexical.models.lexical_record import (
    LexicalRecord,
)
from SanskritAI.lexical.models.lexical_source import (
    LexicalSource,
)


class DictionaryEntry(
    LexicalRecord,
):
    """
    Dictionary-specific lexical record.
    """

    def __init__(
        self,
        identifier: str,
        metadata: DictionaryEntryMetadata,
        source: LexicalSource,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
            source=source,
        )

    # ---------------------------------------------------------
    # Dictionary information
    # ---------------------------------------------------------

    @property
    def dictionary_name(
        self,
    ) -> str:
        return self.metadata.dictionary_name

    @property
    def dictionary_version(
        self,
    ) -> str:
        return self.metadata.dictionary_version

    @property
    def entry_identifier(
        self,
    ) -> str:
        return self.metadata.entry_identifier

    # ---------------------------------------------------------
    # Headword
    # ---------------------------------------------------------

    @property
    def headword(
        self,
    ) -> str:
        return self.metadata.headword

    @property
    def transliteration(
        self,
    ) -> str:
        return self.metadata.transliteration

    # ---------------------------------------------------------
    # Source location
    # ---------------------------------------------------------

    @property
    def volume(
        self,
    ) -> str:
        return self.metadata.volume

    @property
    def chapter(
        self,
    ) -> str:
        return self.metadata.chapter

    @property
    def section(
        self,
    ) -> str:
        return self.metadata.section

    @property
    def page(
        self,
    ) -> str:
        return self.metadata.page

    @property
    def entry_number(
        self,
    ) -> str:
        return self.metadata.entry_number

    # ---------------------------------------------------------
    # Editorial
    # ---------------------------------------------------------

    @property
    def editor(
        self,
    ) -> str:
        return self.metadata.editor

    @property
    def publisher(
        self,
    ) -> str:
        return self.metadata.publisher

    @property
    def publication_year(
        self,
    ) -> str:
        return self.metadata.publication_year

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    @property
    def is_primary(
        self,
    ) -> bool:
        return self.metadata.is_primary

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def citation(
        self,
    ) -> str:
        """
        Human-readable citation.

        Delegates to the metadata object.
        """
        return self.metadata.citation

    @property
    def display_title(
        self,
    ) -> str:
        """
        Preferred title for presentation.
        """
        return self.metadata.display_title
