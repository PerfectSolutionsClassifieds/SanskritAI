
from __future__ import annotations

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
    version: str = "",
    description: str = "",
    publisher: str = "",
    editor: str = "",
    publication_year: str = "",
    website: str = "",
) -> LexicalSource:
    """
    Construct a LexicalSource for validator tests.
    """

    return LexicalSource(
        identifier=identifier,
        name=name,
        version=version,
        description=description,
        publisher=publisher,
        editor=editor,
        publication_year=publication_year,
        website=website,
    )


# ============================================================
# Valid source
# ============================================================


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


# ============================================================
# Whitespace semantics
# ============================================================


def test_whitespace_identifier_is_not_treated_as_empty():
    source = make_lexical_source(
        identifier=" ",
    )

    result = LexicalSourceValidator().validate(source)

    assert result.is_valid


def test_whitespace_name_is_not_treated_as_empty():
    source = make_lexical_source(
        name=" ",
    )

    result = LexicalSourceValidator().validate(source)

    assert result.is_valid


# ============================================================
# Identifier validation — LEX001
# ============================================================


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


# ============================================================
# Name validation — LEX002
# ============================================================


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


# ============================================================
# Multiple validation failures
# ============================================================


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


def test_all_invalid_conditions_report_all_issues():
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


# ============================================================
# Optional source information
# ============================================================


def test_optional_source_information_does_not_affect_validation():
    source = make_lexical_source(
        version="2.1",
        description="Sanskrit lexical source",
        publisher="Classical Texts",
        editor="Editor",
        publication_year="2025",
        website="https://example.org",
    )

    result = LexicalSourceValidator().validate(source)

    assert result.is_valid
    assert result.issues == ()


def test_empty_optional_source_information_is_valid():
    source = make_lexical_source(
        version="",
        description="",
        publisher="",
        editor="",
        publication_year="",
        website="",
    )

    result = LexicalSourceValidator().validate(source)

    assert result.is_valid


# ============================================================
# Display-related model behavior
# ============================================================


def test_display_name_returns_source_name():
    source = make_lexical_source(
        name="Amarakośa",
    )

    assert source.display_name == "Amarakośa"


def test_display_text_without_version_returns_name():
    source = make_lexical_source(
        name="Amarakośa",
        version="",
    )

    assert source.display_text == "Amarakośa"


def test_display_text_with_version_includes_version():
    source = make_lexical_source(
        name="Amarakośa",
        version="1.0",
    )

    assert source.display_text == "Amarakośa (1.0)"


def test_display_description_returns_description():
    source = make_lexical_source(
        description="Canonical Sanskrit lexical source",
    )

    assert source.display_description == (
        "Canonical Sanskrit lexical source"
    )


# ============================================================
# Source information properties
# ============================================================


def test_has_version_is_false_when_version_is_empty():
    source = make_lexical_source(
        version="",
    )

    assert source.has_version is False


def test_has_version_is_true_when_version_is_present():
    source = make_lexical_source(
        version="1.0",
    )

    assert source.has_version is True


def test_has_publisher_is_false_when_publisher_is_empty():
    source = make_lexical_source(
        publisher="",
    )

    assert source.has_publisher is False


def test_has_publisher_is_true_when_publisher_is_present():
    source = make_lexical_source(
        publisher="Publisher",
    )

    assert source.has_publisher is True


def test_has_editor_is_false_when_editor_is_empty():
    source = make_lexical_source(
        editor="",
    )

    assert source.has_editor is False


def test_has_editor_is_true_when_editor_is_present():
    source = make_lexical_source(
        editor="Editor",
    )

    assert source.has_editor is True


def test_has_website_is_false_when_website_is_empty():
    source = make_lexical_source(
        website="",
    )

    assert source.has_website is False


def test_has_website_is_true_when_website_is_present():
    source = make_lexical_source(
        website="https://example.org",
    )

    assert source.has_website is True


# ============================================================
# Validator reuse
# ============================================================


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
