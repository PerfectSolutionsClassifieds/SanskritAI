"""
SanskritAI
==========

LexicalRelation Unit Tests

Version:
    v0.3.0 Final
"""

from models.enums.relation_type import RelationType

from tests.lexical.sample_lexemes import build_relation_demo


def test() -> None:
    """
    Validate LexicalRelation behavior.
    """

    rama, agni = build_relation_demo()

    # ---------------------------------------------------------
    # Basic validation
    # ---------------------------------------------------------

    assert rama.relation_count == 1

    relation = rama.relations[0]

    assert relation.relation_id == "REL-0001"

    assert relation.relation_type == RelationType.RELATED

    assert relation.target_lexeme_id == agni.lexeme_id

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    print("Source Lexeme     :", rama.lemma)

    print("Relation Type     :", relation.relation_type.value)

    print("Target Lexeme ID  :", relation.target_lexeme_id)

    print("Target Lemma      :", agni.lemma)

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    data = relation.to_dict()

    assert data["relation_id"] == "REL-0001"

    assert data["relation_type"] == RelationType.RELATED.value

    assert data["target_lexeme_id"] == agni.lexeme_id

    print()
    print("LexicalRelation test PASSED")


if __name__ == "__main__":
    test()
