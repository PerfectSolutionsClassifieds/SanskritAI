from __future__ import annotations

import pytest

from SanskritAI.lexical.models.lexical_source import (
    LexicalSource,
)
from SanskritAI.lexical.validators.lexical_source_validator import (
    LexicalSourceValidator,
)


def make_lexical_source(
    *,
    identifier: str = "amarakosha",
    name: str = "Amarakosha",
) -> LexicalSource:
    """
    Construct a minimal valid LexicalSource for validator tests.
    """

    return LexicalSource(
        identifier=identifier,
        name=name,
    )


def test_valid_lexical_source_passes_validation():
    source = make_lexical_source()

    result = LexicalSourceValidator().validate(source)

    assert result.is_valid


def test_valid_lexical_source_has_no_validation_errors():
    source = make_lexical_source()

    result = LexicalSourceValidator().validate(source)

    assert result.errors == ()


def test_valid_lexical_source_has_no_issues():
    source = make_lexical_source()

    result = LexicalSourceValidator().validate(source)

    assert result.issues == ()


def test_whitespace_identifier_is_not_treated_as_empty():
    source = make_lexical_source(
        identifier="   ",
    )

    result = LexicalSourceValidator().validate(source)

    assert result.is_valid


def test_whitespace_name_is_not_treated_as_empty():
    source = make_lexical_source(
        name="   ",
    )

    result = LexicalSourceValidator().validate(source)

    assert result.is_valid


def test_missing_identifier_produces_lex001():
    source = make_lexical_source(
        identifier="",
    )

    result = LexicalSourceValidator().validate(source)

    assert not result.is_valid

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX001" in codes


def test_missing_identifier_issue_has_identifier_field():
    source = make_lexical_source(
        identifier="",
    )

    result = LexicalSourceValidator().validate(source)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert issue.field == "identifier"


def test_missing_identifier_issue_has_message():
    source = make_lexical_source(
        identifier="",
    )

    result = LexicalSourceValidator().validate(source)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert "identifier" in issue.message.lower()


def test_missing_name_produces_lex002():
    source = make_lexical_source(
        name="",
    )

    result = LexicalSourceValidator().validate(source)

    assert not result.is_valid

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX002" in codes


def test_missing_name_issue_has_name_field():
    source = make_lexical_source(
        name="",
    )

    result = LexicalSourceValidator().validate(source)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert issue.field == "name"


def test_missing_name_issue_has_message():
    source = make_lexical_source(
        name="",
    )

    result = LexicalSourceValidator().validate(source)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert "name" in issue.message.lower()


def test_missing_metadata_produces_lex003():
    source = make_lexical_source()

    source._metadata = None

    result = LexicalSourceValidator().validate(source)

    assert not result.is_valid

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX003" in codes


def test_missing_metadata_issue_has_metadata_field():
    source = make_lexical_source()

    source._metadata = None

    result = LexicalSourceValidator().validate(source)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX003"
    )

    assert issue.field == "metadata"


def test_missing_metadata_issue_has_message():
    source = make_lexical_source()

    source._metadata = None

    result = LexicalSourceValidator().validate(source)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX003"
    )

    assert "metadata" in issue.message.lower()


def test_empty_identifier_and_missing_name_report_both():
    source = make_lexical_source(
        identifier="",
        name="",
    )

    result = LexicalSourceValidator().validate(source)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX001",
        "LEX002",
    }


def test_empty_identifier_and_missing_metadata_report_both():
    source = make_lexical_source(
        identifier="",
    )

    source._metadata = None

    result = LexicalSourceValidator().validate(source)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX001",
        "LEX003",
    }


def test_empty_name_and_missing_metadata_report_both():
    source = make_lexical_source(
        name="",
    )

    source._metadata = None

    result = LexicalSourceValidator().validate(source)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX002",
        "LEX003",
    }


def test_all_invalid_conditions_report_all_issues():
    source = make_lexical_source(
        identifier="",
        name="",
    )

    source._metadata = None

    result = LexicalSourceValidator().validate(source)

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
    source = make_lexical_source()

    source._metadata = None

    result = LexicalSourceValidator().validate(source)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX003",
    }


def test_validator_can_be_reused():
    validator = LexicalSourceValidator()

    valid = validator.validate(
        make_lexical_source()
    )

    invalid = validator.validate(
        make_lexical_source(
            identifier="",
        )
    )

    assert valid.is_valid
    assert not invalid.is_valid


def test_validator_does_not_retain_previous_issues():
    validator = LexicalSourceValidator()

    invalid = validator.validate(
        make_lexical_source(
            identifier="",
        )
    )

    valid = validator.validate(
        make_lexical_source()
    )

    assert not invalid.is_valid
    assert valid.is_valid
    assert valid.issues == ()


def test_valid_result_contains_no_errors():
    source = make_lexical_source()

    result = LexicalSourceValidator().validate(source)

    assert result.errors == ()
