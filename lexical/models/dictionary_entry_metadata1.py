from __future__ import annotations

"""
SanskritAI
==========

Dictionary Entry Metadata

Metadata describing a lexical entry within a specific
dictionary or lexical resource.

A DictionaryEntry represents how a Lexeme appears in a
particular dictionary (e.g. Amarakośa, Monier-Williams,
Vācaspatyam, Śabdakalpadruma).

Version
-------
v0.3.0
"""

from dataclasses import dataclass

from SanskritAI.lexical.models.base_lexical_metadata import (
    BaseLexicalMetadata,
)


@dataclass(slots=True)
class DictionaryEntryMetadata(BaseLexicalMetadata):
    """
    Metadata describing a dictionary entry.
    """

    # ---------------------------------------------------------
    # Dictionary identification
    # ---------------------------------------------------------

    dictionary_name: str = ""

    dictionary_version: str = ""

    entry_identifier: str = ""

    # ---------------------------------------------------------
    # Headword information
    # ---------------------------------------------------------

    headword: str = ""

    transliteration: str = ""

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
