"""
SanskritAI
==========

Module:
    tests.lexical.sample_lexemes

Description:
    Factory functions providing reusable lexical objects
    for unit tests.

Version:
    v0.3.0 Final
"""

from __future__ import annotations

from models.enums.dictionary_source import DictionarySource
from models.enums.language import Language
from models.enums.relation_type import RelationType
from models.enums.script import Script

from models.lexical import (
    DictionaryEntry,
    DictionarySense,
    Lexeme,
    LexicalRelation,
)


def create_rama() -> Lexeme:
    """
    Create a sample Lexeme representing राम.
    """

    sense = DictionarySense(
        sense_id="SENSE-RAMA-001",
        definition="Rāma, hero of the Rāmāyaṇa.",
    )

    entry = DictionaryEntry(
        entry_id="ENTRY-RAMA-AMARA",
        source=DictionarySource.AMARAKOSHA,
        headword="राम",
        senses=[sense],
    )

    lexeme = Lexeme(
        lexeme_id="LEX-RAMA",
        lemma="राम",
        transliteration="rāma",
        language=Language.SANSKRIT,
        script=Script.DEVANAGARI,
    )

    lexeme.add_dictionary_entry(entry)

    return lexeme


def create_agni() -> Lexeme:
    """
    Create a sample Lexeme representing अग्नि.
    """

    sense = DictionarySense(
        sense_id="SENSE-AGNI-001",
        definition="Fire; the Vedic deity Agni.",
    )

    entry = DictionaryEntry(
        entry_id="ENTRY-AGNI-AMARA",
        source=DictionarySource.AMARAKOSHA,
        headword="अग्नि",
        senses=[sense],
    )

    lexeme = Lexeme(
        lexeme_id="LEX-AGNI",
        lemma="अग्नि",
        transliteration="agni",
        language=Language.SANSKRIT,
        script=Script.DEVANAGARI,
    )

    lexeme.add_dictionary_entry(entry)

    return lexeme


def build_relation_demo() -> tuple[Lexeme, Lexeme]:
    """
    Create two related Lexeme objects for testing.
    """

    rama = create_rama()
    agni = create_agni()

    relation = LexicalRelation(
        relation_id="REL-0001",
        relation_type=RelationType.RELATED,
        target_lexeme_id=agni.lexeme_id,
    )

    rama.add_relation(relation)

    return rama, agni
