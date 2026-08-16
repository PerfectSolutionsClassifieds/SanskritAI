from __future__ import annotations

import pytest

from SanskritAI.domain.lexical.lexical_relation import LexicalRelation
from SanskritAI.domain.lexical.validators.lexical_relation_validator import (
    LexicalRelationValidator,
)
from SanskritAI.models.enums.relation_type import RelationType


def make_relation(
    *,
    relation_id: str = "relation-1",
    source_lexeme_id: str = "lexeme-1",
    relation_type: RelationType = RelationType.SYNONYM,
    target_lexeme_id: str = "lexeme-2",
    notes: str = "",
) -> LexicalRelation:
    return LexicalRelation(
        relation_id=relation_id,
        source_lexeme_id=source_lexeme_id,
        relation_type=relation_type,
        target_lexeme_id=target_lexeme_id,
        notes=notes,
    )


def issue_codes(result):
    return {issue.code for issue in result.issues}


def test_supports_lexical_relation():
    relation = make_relation()

    assert LexicalRelationValidator.supports(relation) is True


def test_does_not_support_unrelated_object():
    assert LexicalRelationValidator.supports(object()) is False


def test_valid_relation_passes():
    result = LexicalRelationValidator().validate(
        make_relation()
    )

    assert result.is_valid


def test_empty_relation_id_is_invalid():
    relation = make_relation(relation_id="")

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid
    assert "LEXREL001" in issue_codes(result)


def test_blank_relation_id_is_invalid():
    relation = make_relation(relation_id="   ")

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid
    assert "LEXREL001" in issue_codes(result)


def test_empty_source_lexeme_id_is_invalid():
    relation = make_relation(source_lexeme_id="")

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid
    assert "LEXREL002" in issue_codes(result)


def test_blank_source_lexeme_id_is_invalid():
    relation = make_relation(source_lexeme_id="   ")

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid
    assert "LEXREL002" in issue_codes(result)


def test_empty_target_lexeme_id_is_invalid():
    relation = make_relation(target_lexeme_id="")

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid
    assert "LEXREL004" in issue_codes(result)


def test_blank_target_lexeme_id_is_invalid():
    relation = make_relation(target_lexeme_id="   ")

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid
    assert "LEXREL004" in issue_codes(result)


def test_self_relation_produces_warning():
    relation = make_relation(
        source_lexeme_id="lexeme-1",
        target_lexeme_id="lexeme-1",
    )

    result = LexicalRelationValidator().validate(relation)

    assert result.is_valid
    assert "LEXREL005" in issue_codes(result)


def test_notes_are_optional():
    relation = make_relation(notes="")

    result = LexicalRelationValidator().validate(relation)

    assert result.is_valid


def test_relation_type_is_preserved():
    relation = make_relation(
        relation_type=RelationType.ANTONYM,
    )

    assert relation.relation_type is RelationType.ANTONYM


def test_relation_identity_is_stable():
    relation = make_relation(
        source_lexeme_id="lexeme-a",
        relation_type=RelationType.SYNONYM,
        target_lexeme_id="lexeme-b",
    )

    assert relation.identity == (
        "lexeme-a",
        RelationType.SYNONYM,
        "lexeme-b",
    )


def test_relation_to_dict_is_json_compatible():
    relation = make_relation(
        notes="semantic relation",
    )

    data = relation.to_dict()

    assert data["relation_id"] == "relation-1"
    assert data["source_lexeme_id"] == "lexeme-1"
    assert data["relation_type"] == "synonym"
    assert data["target_lexeme_id"] == "lexeme-2"
    assert data["notes"] == "semantic relation"


def test_display_name_uses_relation_type():
    relation = make_relation(
        relation_type=RelationType.SYNONYM,
    )

    assert relation.display_name == "synonym"


def test_display_text_contains_relation():
    relation = make_relation(
        source_lexeme_id="lexeme-a",
        relation_type=RelationType.ANTONYM,
        target_lexeme_id="lexeme-b",
    )

    assert relation.display_text == (
        "lexeme-a antonym lexeme-b"
    )


def test_string_representation_uses_display_text():
    relation = make_relation()

    assert str(relation) == relation.display_text


def test_relation_is_immutable():
    relation = make_relation()

    with pytest.raises((AttributeError, TypeError)):
        relation.notes = "changed"


def test_relation_normalizes_text_fields():
    relation = make_relation(
        relation_id="  relation-1  ",
        source_lexeme_id="  lexeme-1  ",
        target_lexeme_id="  lexeme-2  ",
        notes="  note  ",
    )

    assert relation.relation_id == "relation-1"
    assert relation.source_lexeme_id == "lexeme-1"
    assert relation.target_lexeme_id == "lexeme-2"
    assert relation.notes == "note"
