from __future__ import annotations

"""
SanskritAI
==========

Dictionary Entry Builder

Fluent builder for DictionaryEntry objects.

Version
-------
v0.3.0
"""

from SanskritAI.lexical.builders.base_lexical_builder import (
    BaseLexicalBuilder,
)
from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)
from SanskritAI.lexical.models.dictionary_entry_metadata import (
    DictionaryEntryMetadata,
)


class DictionaryEntryBuilder(
    BaseLexicalBuilder[DictionaryEntry],
):
    """
    Fluent builder for DictionaryEntry.
    """

    def __init__(self) -> None:
        super().__init__()

        self._identifier = ""
        self._metadata = DictionaryEntryMetadata()

    # ---------------------------------------------------------

    def with_identifier(
        self,
        identifier: str,
    ) -> "DictionaryEntryBuilder":

        self._identifier = identifier
        return self

    # ---------------------------------------------------------

    def with_dictionary(
        self,
        name: str,
        version: str = "",
    ) -> "DictionaryEntryBuilder":

        self._metadata.dictionary_name = name
        self._metadata.dictionary_version = version
        return self

    # ---------------------------------------------------------

    def with_headword(
        self,
        headword: str,
    ) -> "DictionaryEntryBuilder":

        self._metadata.headword = headword
        return self

    # ---------------------------------------------------------

    def with_transliteration(
        self,
        transliteration: str,
    ) -> "DictionaryEntryBuilder":

        self._metadata.transliteration = transliteration
        return self

    # ---------------------------------------------------------

    def with_entry_identifier(
        self,
        entry_identifier: str,
    ) -> "DictionaryEntryBuilder":

        self._metadata.entry_identifier = entry_identifier
        return self

    # ---------------------------------------------------------

    def build(self) -> DictionaryEntry:

        return DictionaryEntry(
            identifier=self._identifier,
            metadata=self._metadata,
        )
