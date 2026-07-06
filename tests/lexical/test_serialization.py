"""
SanskritAI
==========

Lexical Serialization Tests

Version:
    v0.3.0 Final
"""

from tests.lexical.sample_lexemes import (
    create_rama,
    build_relation_demo,
)


def test() -> None:
    """
    Validate serialization of lexical objects.
    """

    # ---------------------------------------------------------
    # Lexeme serialization
    # ---------------------------------------------------------

    rama = create_rama()

    data = rama.to_dict()

    assert isinstance(data, dict)

    assert data["lexeme_id"] == "LEX-RAMA"

    assert data["lemma"] == "राम"

    assert len(data["dictionary_entries"]) == 1

    assert len(data["relations"]) == 0

    print("Lexeme serialization PASSED")

    # ---------------------------------------------------------
    # Relation serialization
    # ---------------------------------------------------------

    rama, agni = build_relation_demo()

    relation = rama.relations[0]

    relation_data = relation.to_dict()

    assert relation_data["target_lexeme_id"] == agni.lexeme_id

    print("Relation serialization PASSED")

    # ---------------------------------------------------------
    # DictionaryEntry serialization
    # ---------------------------------------------------------

    entry = rama.dictionary_entries[0]

    entry_data = entry.to_dict()

    assert entry_data["headword"] == "राम"

    assert entry_data["sense_count"] == 1

    print("DictionaryEntry serialization PASSED")

    # ---------------------------------------------------------
    # DictionarySense serialization
    # ---------------------------------------------------------

    sense = entry.senses[0]

    sense_data = sense.to_dict()

    assert sense_data["definition"]

    print("DictionarySense serialization PASSED")

    print()
    print("Serialization test PASSED")


if __name__ == "__main__":
    test()
