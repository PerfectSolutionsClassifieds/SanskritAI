from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.dictionary_entry import DictionaryEntry
from SanskritAI.lexical.models.dictionary_sense import DictionarySense
from SanskritAI.lexical.models.lexical_relation import LexicalRelation
from SanskritAI.lexical.models.lexeme_metadata import LexemeMetadata
from SanskritAI.lexical.models.dictionary_entry_metadata import DictionaryEntryMetadata
from SanskritAI.lexical.models.dictionary_sense_metadata import DictionarySenseMetadata
from SanskritAI.lexical.models.lexical_relation_metadata import LexicalRelationMetadata
from SanskritAI.lexical.registries.lexical_registry import LexicalRegistry
from SanskritAI.lexical.enums.relation_type import RelationType


def make_lexeme(identifier="lexeme-1"):
    return Lexeme(
        identifier=identifier,
        metadata=LexemeMetadata(
            lemma="राम",
            transliteration="rāma",
        ),
    )


def make_dictionary_entry(identifier="entry-1"):
    return DictionaryEntry(
        identifier=identifier,
        metadata=DictionaryEntryMetadata(
            lemma="राम",
        ),
    )


def make_dictionary_sense(identifier="sense-1"):
    return DictionarySense(
        identifier=identifier,
        metadata=DictionarySenseMetadata(
            definition="Rāma",
        ),
    )


def make_lexical_relation(identifier="relation-1"):
    return LexicalRelation(
        identifier=identifier,
        metadata=LexicalRelationMetadata(
            relation_type=RelationType.RELATED,
            source_identifier="lexeme-1",
            target_identifier="entry-1",
        ),
    )


def test_registry_starts_empty():
    registry = LexicalRegistry()
    assert len(registry) == 0
    assert list(registry.values()) == []
    assert list(registry.identifiers()) == []


def test_registers_lexical_object():
    registry = LexicalRegistry()
    lexeme = make_lexeme()

    registry.register(lexeme)

    assert len(registry) == 1
    assert registry.get(lexeme.id) is lexeme


def test_register_many_registers_all_objects():
    registry = LexicalRegistry()
    objects = [
        make_lexeme(),
        make_dictionary_entry(),
        make_dictionary_sense(),
        make_lexical_relation(),
    ]

    registry.register_many(objects)

    assert len(registry) == 4
    for obj in objects:
        assert registry.get(obj.id) is obj


def test_lookup_unknown_identifier_returns_none():
    registry = LexicalRegistry()

    assert registry.get("does-not-exist") is None


def test_exists_reports_registered_identifier():
    registry = LexicalRegistry()
    lexeme = make_lexeme()

    assert not registry.exists(lexeme.id)

    registry.register(lexeme)

    assert registry.exists(lexeme.id)


def test_remove_removes_registered_object():
    registry = LexicalRegistry()
    lexeme = make_lexeme()

    registry.register(lexeme)
    registry.remove(lexeme.id)

    assert not registry.exists(lexeme.id)
    assert registry.get(lexeme.id) is None


def test_clear_removes_all_objects():
    registry = LexicalRegistry()
    registry.register_many(
        [
            make_lexeme(),
            make_dictionary_entry(),
            make_dictionary_sense(),
            make_lexical_relation(),
        ]
    )

    registry.clear()

    assert len(registry) == 0
    assert list(registry.values()) == []


def test_identifiers_returns_registered_identifiers():
    registry = LexicalRegistry()
    objects = [
        make_lexeme(),
        make_dictionary_entry(),
    ]

    registry.register_many(objects)

    assert set(registry.identifiers()) == {
        "lexeme-1",
        "entry-1",
    }


def test_items_returns_identifier_object_pairs():
    registry = LexicalRegistry()
    lexeme = make_lexeme()

    registry.register(lexeme)

    assert list(registry.items()) == [
        (lexeme.id, lexeme),
    ]


def test_iteration_returns_registered_objects():
    registry = LexicalRegistry()
    lexeme = make_lexeme()
    entry = make_dictionary_entry()

    registry.register_many([lexeme, entry])

    assert list(registry) == [lexeme, entry]


def test_lexemes_returns_only_lexemes():
    registry = LexicalRegistry()
    lexeme = make_lexeme()

    registry.register_many(
        [
            lexeme,
            make_dictionary_entry(),
            make_dictionary_sense(),
            make_lexical_relation(),
        ]
    )

    assert list(registry.lexemes()) == [lexeme]


def test_dictionary_entries_returns_only_dictionary_entries():
    registry = LexicalRegistry()
    entry = make_dictionary_entry()

    registry.register_many(
        [
            make_lexeme(),
            entry,
            make_dictionary_sense(),
            make_lexical_relation(),
        ]
    )

    assert list(registry.dictionary_entries()) == [entry]


def test_dictionary_senses_returns_only_dictionary_senses():
    registry = LexicalRegistry()
    sense = make_dictionary_sense()

    registry.register_many(
        [
            make_lexeme(),
            make_dictionary_entry(),
            sense,
            make_lexical_relation(),
        ]
    )

    assert list(registry.dictionary_senses()) == [sense]


def test_lexical_relations_returns_only_lexical_relations():
    registry = LexicalRegistry()
    relation = make_lexical_relation()

    registry.register_many(
        [
            make_lexeme(),
            make_dictionary_entry(),
            make_dictionary_sense(),
            relation,
        ]
    )

    assert list(registry.lexical_relations()) == [relation]


def test_typed_projections_are_empty_when_no_matching_objects_exist():
    registry = LexicalRegistry()
    registry.register(make_lexeme())

    assert list(registry.dictionary_entries()) == []
    assert list(registry.dictionary_senses()) == []
    assert list(registry.lexical_relations()) == []
