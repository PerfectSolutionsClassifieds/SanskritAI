from __future__ import annotations

"""
SanskritAI
==========

Lexical Source

Represents the canonical source of lexical knowledge.

A LexicalSource identifies the origin from which lexical
information is derived. It is intentionally generic and is
not limited to traditional dictionaries.

Examples
--------

Amarakośa

Monier-Williams

Vācaspatyam

Śabdakalpadruma

Apte

Digital Corpus of Sanskrit

Paninian Dhātupāṭha

Future relationships
--------------------

LexicalSource
    ├── DictionaryEntry
    ├── DictionarySense
    ├── Lexeme
    └── LexicalRepository

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class LexicalSource(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Immutable lexical source.
    """

    identifier: str

    name: str

    version: str = ""

    description: str = ""

    publisher: str = ""

    editor: str = ""

    publication_year: str = ""

    website: str = ""

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def display_text(self) -> str:
        if self.version:
            return f"{self.name} ({self.version})"
        return self.name

    @property
    def display_description(self) -> str:
        return self.description

    @property
    def has_version(self) -> bool:
        return bool(self.version)

    @property
    def has_publisher(self) -> bool:
        return bool(self.publisher)

    @property
    def has_editor(self) -> bool:
        return bool(self.editor)

    @property
    def has_website(self) -> bool:
        return bool(self.website)

    def __str__(self) -> str:
        return self.display_text
