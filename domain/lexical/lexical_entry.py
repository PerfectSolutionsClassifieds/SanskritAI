from __future__ import annotations

"""
SanskritAI
==========

Lexical Entry

Aggregate Root of the Lexical Kernel.

A LexicalEntry represents the complete linguistic knowledge
known about a single lexical concept.

It intentionally aggregates multiple lexical resources while
remaining independent of any one dictionary.

Relationship
------------

LexicalEntry
    │
    ├── Lexeme
    ├── DictionaryEntryCollection
    ├── DictionarySenseCollection
    ├── WordFormCollection
    └── LexicalRelationCollection

Version
-------
v1.0.0
"""

from dataclasses import dataclass

from SanskritAI.core.mixins.displayable import Displayable
from SanskritAI.core.mixins.immutable import Immutable
from SanskritAI.core.value_objects.value_object import ValueObject

from SanskritAI.lexical.models.lexeme import Lexeme

from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)

from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)

from SanskritAI.lexical.models.lexical_relation import (
    LexicalRelation,
)

from SanskritAI.domain.lexical.word_form import WordForm


@dataclass(frozen=True, slots=True)
class LexicalEntry(
    ValueObject,
    Immutable,
    Displayable,
):
    """
    Aggregate Root of the Lexical Kernel.
    """

    identifier: str

    lexeme: Lexeme

    dictionary_entries: tuple[
        DictionaryEntry,
        ...
    ] = ()

    dictionary_senses: tuple[
        DictionarySense,
        ...
    ] = ()

    word_forms: tuple[
        WordForm,
        ...
    ] = ()

    relations: tuple[
        LexicalRelation,
        ...
    ] = ()

    notes: str = ""

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self.lexeme.display_name

    @property
    def display_text(self) -> str:
        return self.lexeme.display_text

    @property
    def display_description(self) -> str:
        return self.notes

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    @property
    def lemma(self) -> str:
        return self.lexeme.lemma

    @property
    def entry_count(self) -> int:
        return len(self.dictionary_entries)

    @property
    def sense_count(self) -> int:
        return len(self.dictionary_senses)

    @property
    def word_form_count(self) -> int:
        return len(self.word_forms)

    @property
    def relation_count(self) -> int:
        return len(self.relations)

    @property
    def has_dictionary_entries(self) -> bool:
        return bool(self.dictionary_entries)

    @property
    def has_dictionary_senses(self) -> bool:
        return bool(self.dictionary_senses)

    @property
    def has_word_forms(self) -> bool:
        return bool(self.word_forms)

    @property
    def has_relations(self) -> bool:
        return bool(self.relations)

    def __str__(self) -> str:
        return self.display_text
