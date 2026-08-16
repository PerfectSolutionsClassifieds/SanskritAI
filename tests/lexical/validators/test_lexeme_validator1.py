from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexeme_metadata import LexemeMetadata
from SanskritAI.lexical.validators.lexeme_validator import LexemeValidator


def make_lexeme(
    identifier="lexeme-1",
    metadata=None,
):
    if metadata is None:
        metadata = LexemeMetadata(
            lemma="राम",
            transliteration="rāma",
        )

    return Lexeme(
        identifier=identifier,
        metadata=metadata,
    )


def test_valid_lexeme_passes_validation():
    lexeme = make_lexeme()

    result = LexemeValidator().validate(lexeme)

    assert result.is_valid
    assert result.issues == ()


def test_valid_lexeme_has_no_validation_errors():
    lexeme = make_lexeme()

    result = LexemeValidator().validate(lexeme)

    assert result.errors == ()


def test_empty_identifier_produces_lex001():
    lexeme = make_lexeme(identifier="")

    result = LexemeValidator().validate(lexeme)

    assert not result.is_valid
    assert any(
        issue.code == "LEX001"
        for issue in result.issues
    )


def test_empty_identifier_issue_has_identifier_field():
    lexeme = make_lexeme(identifier="")

    result = LexemeValidator().validate(lexeme)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert issue.field == "identifier"


def test_empty_identifier_issue_has_message():
    lexeme = make_lexeme(identifier="")

    result = LexemeValidator().validate(lexeme)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert issue.message


def test_missing_metadata_produces_lex002():
    lexeme = make_lexeme()
    lexeme._metadata = None

    result = LexemeValidator().validate(lexeme)

    assert not result.is_valid
    assert any(
        issue.code == "LEX002"
        for issue in result.issues
    )


def test_missing_metadata_issue_has_metadata_field():
    lexeme = make_lexeme()
    lexeme._metadata = None

    result = LexemeValidator().validate(lexeme)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert issue.field == "metadata"


def test_missing_metadata_issue_has_message():
    lexeme = make_lexeme()
    lexeme._metadata = None

    result = LexemeValidator().validate(lexeme)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert issue.message


def test_empty_identifier_and_missing_metadata_report_both_issues():
    lexeme = make_lexeme(identifier="")
    lexeme._metadata = None

    result = LexemeValidator().validate(lexeme)

    codes = {issue.code for issue in result.issues}

    assert "LEX001" in codes
    assert "LEX002" in codes


def test_validation_returns_validation_result():
    lexeme = make_lexeme()

    result = LexemeValidator().validate(lexeme)

    assert result is not None
    assert hasattr(result, "is_valid")
    assert hasattr(result, "issues")


def test_validator_can_be_reused():
    validator = LexemeValidator()

    valid = validator.validate(make_lexeme())
    invalid = validator.validate(make_lexeme(identifier=""))

    assert valid.is_valid
    assert not invalid.is_valid


def test_validator_accepts_lexeme_with_metadata_values():
    lexeme = make_lexeme(
        metadata=LexemeMetadata(
            lemma="नर",
            transliteration="nara",
        )
    )

    result = LexemeValidator().validate(lexeme)

    assert result.is_valid


def test_validation_does_not_modify_valid_lexeme():
    lexeme = make_lexeme()

    identifier = lexeme.id
    metadata = lexeme.metadata

    LexemeValidator().validate(lexeme)

    assert lexeme.id == identifier
    assert lexeme.metadata is metadata


def test_validation_does_not_modify_invalid_lexeme():
    lexeme = make_lexeme(identifier="")
    metadata = lexeme.metadata

    LexemeValidator().validate(lexeme)

    assert lexeme.id == ""
    assert lexeme.metadata is metadata
