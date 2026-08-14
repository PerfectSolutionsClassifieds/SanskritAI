from __future__ import annotations

from SanskritAI.lexical.enums.relation_type import RelationType
from SanskritAI.lexical.models.lexical_relation import (
    LexicalRelation,
)
from SanskritAI.lexical.models.lexical_relation_metadata import (
    LexicalRelationMetadata,
)
from SanskritAI.lexical.validators.lexical_relation_validator import (
    LexicalRelationValidator,
)


# =============================================================
# Helpers
# =============================================================


def make_metadata(
    *,
    source_identifier: str = "lexeme-1",
    target_identifier: str = "lexeme-2",
) -> LexicalRelationMetadata:
    return LexicalRelationMetadata(
        relation_type=RelationType.RELATED,
        source_identifier=source_identifier,
        target_identifier=target_identifier,
        directed=True,
        weight=1.0,
        confidence=1.0,
        source_dictionary="test-dictionary",
        notes="",
    )


def make_lexical_relation(
    *,
    identifier: str = "relation-1",
    metadata: LexicalRelationMetadata | None = None,
) -> LexicalRelation:
    if metadata is None:
        metadata = make_metadata()

    return LexicalRelation(
        identifier=identifier,
        metadata=metadata,
    )


# =============================================================
# Valid relation
# =============================================================


def test_valid_lexical_relation_passes_validation():
    relation = make_lexical_relation()

    result = LexicalRelationValidator().validate(relation)

    assert result.is_valid


def test_valid_lexical_relation_has_no_validation_errors():
    relation = make_lexical_relation()

    result = LexicalRelationValidator().validate(relation)

    assert result.errors == ()


def test_valid_lexical_relation_has_no_issues():
    relation = make_lexical_relation()

    result = LexicalRelationValidator().validate(relation)

    assert result.issues == ()


def test_whitespace_identifier_is_not_treated_as_empty():
    relation = make_lexical_relation(
        identifier="   ",
    )

    result = LexicalRelationValidator().validate(relation)

    assert result.is_valid


# =============================================================
# LEX001 — Identifier
# =============================================================


def test_missing_identifier_produces_lex001():
    relation = make_lexical_relation(
        identifier="",
    )

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX001" in codes


def test_missing_identifier_issue_has_identifier_field():
    relation = make_lexical_relation(
        identifier="",
    )

    result = LexicalRelationValidator().validate(relation)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert issue.field == "identifier"


def test_missing_identifier_issue_has_message():
    relation = make_lexical_relation(
        identifier="",
    )

    result = LexicalRelationValidator().validate(relation)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert (
        issue.message
        == "Lexical relation identifier must not be empty."
    )


# =============================================================
# LEX002 — Source identifier
# =============================================================


def test_missing_source_identifier_produces_lex002():
    relation = make_lexical_relation(
        metadata=make_metadata(
            source_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX002" in codes


def test_missing_source_identifier_issue_has_source_field():
    relation = make_lexical_relation(
        metadata=make_metadata(
            source_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert issue.field == "source_identifier"


def test_missing_source_identifier_issue_has_message():
    relation = make_lexical_relation(
        metadata=make_metadata(
            source_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert (
        issue.message
        == "Lexical relation source identifier must not be empty."
    )


# =============================================================
# LEX003 — Target identifier
# =============================================================


def test_missing_target_identifier_produces_lex003():
    relation = make_lexical_relation(
        metadata=make_metadata(
            target_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX003" in codes


def test_missing_target_identifier_issue_has_target_field():
    relation = make_lexical_relation(
        metadata=make_metadata(
            target_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX003"
    )

    assert issue.field == "target_identifier"


def test_missing_target_identifier_issue_has_message():
    relation = make_lexical_relation(
        metadata=make_metadata(
            target_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX003"
    )

    assert (
        issue.message
        == "Lexical relation target identifier must not be empty."
    )


# =============================================================
# LEX004 — Metadata
# =============================================================


def test_missing_metadata_produces_lex004():
    relation = make_lexical_relation()

    relation._metadata = None

    result = LexicalRelationValidator().validate(relation)

    assert not result.is_valid

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX004" in codes


def test_missing_metadata_issue_has_metadata_field():
    relation = make_lexical_relation()

    relation._metadata = None

    result = LexicalRelationValidator().validate(relation)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX004"
    )

    assert issue.field == "metadata"


def test_missing_metadata_issue_has_message():
    relation = make_lexical_relation()

    relation._metadata = None

    result = LexicalRelationValidator().validate(relation)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX004"
    )

    assert (
        issue.message
        == "Lexical relation metadata is required."
    )


# =============================================================
# Combined failures
# =============================================================


def test_empty_identifier_and_missing_source_report_both():
    relation = make_lexical_relation(
        identifier="",
        metadata=make_metadata(
            source_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX001" in codes
    assert "LEX002" in codes


def test_empty_identifier_and_missing_target_report_both():
    relation = make_lexical_relation(
        identifier="",
        metadata=make_metadata(
            target_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX001" in codes
    assert "LEX003" in codes


def test_missing_source_and_target_report_both():
    relation = make_lexical_relation(
        metadata=make_metadata(
            source_identifier="",
            target_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX002",
        "LEX003",
    }


def test_empty_identifier_and_missing_metadata_report_both():
    relation = make_lexical_relation(
        identifier="",
    )

    relation._metadata = None

    result = LexicalRelationValidator().validate(relation)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX001",
        "LEX004",
    }


def test_all_invalid_conditions_report_all_issues():
    relation = make_lexical_relation(
        identifier="",
        metadata=make_metadata(
            source_identifier="",
            target_identifier="",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX001",
        "LEX002",
        "LEX003",
    }


def test_missing_metadata_does_not_attempt_child_metadata_validation():
    relation = make_lexical_relation()

    relation._metadata = None

    result = LexicalRelationValidator().validate(relation)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX004",
    }


# =============================================================
# Metadata values
# =============================================================


def test_validator_accepts_relation_with_metadata_values():
    relation = make_lexical_relation(
        metadata=LexicalRelationMetadata(
            relation_type=RelationType.RELATED,
            source_identifier="राम",
            target_identifier="नारायण",
            directed=True,
            weight=0.75,
            confidence=0.95,
            source_dictionary="Amarakosha",
            notes="semantic relation",
        ),
    )

    result = LexicalRelationValidator().validate(relation)

    assert result.is_valid


# =============================================================
# Validator lifecycle
# =============================================================


def test_validator_can_be_reused():
    validator = LexicalRelationValidator()

    valid = validator.validate(
        make_lexical_relation()
    )

    invalid = validator.validate(
        make_lexical_relation(
            identifier="",
        )
    )

    assert valid.is_valid
    assert not invalid.is_valid


def test_validator_does_not_retain_previous_issues():
    validator = LexicalRelationValidator()

    invalid = validator.validate(
        make_lexical_relation(
            identifier="",
        )
    )

    valid = validator.validate(
        make_lexical_relation()
    )

    assert not invalid.is_valid
    assert valid.is_valid
    assert valid.issues == ()


def test_valid_result_contains_no_errors():
    relation = make_lexical_relation()

    result = LexicalRelationValidator().validate(relation)

    assert result.errors == ()
