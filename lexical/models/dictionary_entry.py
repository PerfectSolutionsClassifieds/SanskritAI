from __future__ import annotations

"""
SanskritAI
==========

Dictionary Entry

Represents a lexical entry from a specific dictionary.

A DictionaryEntry belongs to a particular lexical resource
(e.g. Amarakośa, Monier-Williams, Apte, Vācaspatyam,
Śabdakalpadruma).

It describes how a Lexeme appears within that resource.

Hierarchy
---------

Lexeme
    ├── DictionaryEntry
    ├── DictionaryEntry
    └── DictionaryEntry

Dictionary senses are modeled separately by
DictionarySense.

Version
-------
v0.3.0
"""

from SanskritAI.lexical.models.base_lexical_node import (
    BaseLexicalNode,
)

from SanskritAI.lexical.models.dictionary_entry_metadata import (
    DictionaryEntryMetadata,
)


class DictionaryEntry(
    BaseLexicalNode[
        str,
        DictionaryEntryMetadata,
    ]
):
    """
    Dictionary-specific lexical entry.
    """

    def __init__(
        self,
        identifier: str,
        metadata: DictionaryEntryMetadata,
    ) -> None:

        super().__init__(
            identifier=identifier,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Dictionary Information
    # ---------------------------------------------------------

    @property
    def dictionary_name(
        self,
    ) -> str:
        """
        Dictionary name.
        """

        return self.metadata.dictionary_name

    # ---------------------------------------------------------

    @property
    def dictionary_version(
        self,
    ) -> str:
        """
        Dictionary edition/version.
        """

        return self.metadata.dictionary_version

    # ---------------------------------------------------------

    @property
    def entry_identifier(
        self,
    ) -> str:
        """
        Dictionary-specific entry identifier.
        """

        return self.metadata.entry_identifier

    # ---------------------------------------------------------
    # Headword
    # ---------------------------------------------------------

    @property
    def headword(
        self,
    ) -> str:
        """
        Headword as presented in the dictionary.
        """

        return self.metadata.headword

    # ---------------------------------------------------------

    @property
    def transliteration(
        self,
    ) -> str:
        """
        Transliterated headword.
        """

        return self.metadata.transliteration

    # ---------------------------------------------------------
    # Source Location
    # ---------------------------------------------------------

    @property
    def volume(
        self,
    ) -> str:
        """
        Source volume.
        """

        return self.metadata.volume

    # ---------------------------------------------------------

    @property
    def chapter(
        self,
    ) -> str:
        """
        Source chapter.
        """

        return self.metadata.chapter

    # ---------------------------------------------------------

    @property
    def section(
        self,
    ) -> str:
        """
        Source section.
        """

        return self.metadata.section

    # ---------------------------------------------------------

    @property
    def page(
        self,
    ) -> str:
        """
        Source page.
        """

        return self.metadata.page

    # ---------------------------------------------------------

    @property
    def entry_number(
        self,
    ) -> str:
        """
        Entry number.
        """

        return self.metadata.entry_number

    # ---------------------------------------------------------
    # Editorial
    # ---------------------------------------------------------

    @property
    def editor(
        self,
    ) -> str:
        """
        Editor.
        """

        return self.metadata.editor

    # ---------------------------------------------------------

    @property
    def publisher(
        self,
    ) -> str:
        """
        Publisher.
        """

        return self.metadata.publisher

    # ---------------------------------------------------------

    @property
    def publication_year(
        self,
    ) -> str:
        """
        Publication year.
        """

        return self.metadata.publication_year

    # ---------------------------------------------------------

    @property
    def is_primary(
        self,
    ) -> bool:
        """
        Indicates whether this is the preferred
        dictionary entry.
        """

        return self.metadata.is_primary
