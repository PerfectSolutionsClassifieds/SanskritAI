
from __future__ import annotations

import pytest

from SanskritAI.core.validators.validation_issue import (
    ValidationSeverity,
)
from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.domain.lexical.lexeme import Lexeme
from SanskritAI.domain.lexical.validators.lexeme_validator import (
    LexemeValidator,
)


def make_lexeme(
    *,
    identifier: str = "lexeme-1",
    lemma: str = "राम",
    language: str = "sanskrit",
    script: str = "devanagari",
    transliteration: str = "rāma",
    description: str = "",
    aliases: frozenset[str] | None = None,
) -> Lexeme:
    if aliases is None:
        aliases = frozenset()

    return Lexeme(
        identifier=identifier,
        lemma=lemma,
        language=language,
        script=script,
        transliteration=transliteration,
        description=description,
        aliases=aliases,
    )


# =============================================================
# Basic validation
# =============================================================


def test_valid_lexeme_passes_validation():
    result = LexemeValidator().validate(make_lexeme())

    assert isinstance(result, ValidationResult)
    assert result.is_valid
    assert result.issues == ()


def test_valid_lexeme_has_no_errors():
    result = LexemeValidator().validate(make_lexeme())

    assert result.errors == ()
    assert result.error_count == 0


def test_validator_supports_lexeme():
    lexeme = make_lexeme()

    assert LexemeValidator.supports(lexeme) is True


def test_validator_does_not_support_arbitrary_object():
    assert LexemeValidator.supports(object()) is False


# =============================================================
# Identifier
# =============================================================


def test_empty_identifier_produces_lex001():
    result = LexemeValidator().validate(
        make_lexeme(identifier="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "LEX001"
        for issue in result.issues
    )


def test_whitespace_identifier_produces_lex001():
    result = LexemeValidator().validate(
        make_lexeme(identifier="   ")
    )

    assert not result.is_valid
    assert any(
        issue.code == "LEX001"
        for issue in result.issues
    )


def test_identifier_issue_targets_identifier_field():
    result = LexemeValidator().validate(
        make_lexeme(identifier="")
    )

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert issue.field == "identifier"
    assert issue.severity == ValidationSeverity.ERROR
    assert issue.message


# =============================================================
# Lemma
# =============================================================


def test_empty_lemma_produces_lex002():
    result = LexemeValidator().validate(
        make_lexeme(lemma="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "LEX002"
        for issue in result.issues
    )


def test_whitespace_lemma_produces_lex002():
    result = LexemeValidator().validate(
        make_lexeme(lemma="   ")
    )

    assert not result.is_valid
    assert any(
        issue.code == "LEX002"
        for issue in result.issues
    )


def test_lemma_issue_targets_lemma_field():
    result = LexemeValidator().validate(
        make_lexeme(lemma="")
    )

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert issue.field == "lemma"


# =============================================================
# Language / script
# =============================================================


def test_empty_language_produces_lex003():
    result = LexemeValidator().validate(
        make_lexeme(language="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "LEX003"
        for issue in result.issues
    )


def test_empty_script_produces_lex004():
    result = LexemeValidator().validate(
        make_lexeme(script="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "LEX004"
        for issue in result.issues
    )


def test_default_language_and_script_are_valid():
    lexeme = Lexeme(
        identifier="lexeme-1",
        lemma="धर्म",
    )

    result = LexemeValidator().validate(lexeme)

    assert result.is_valid


# =============================================================
# Optional textual fields
# =============================================================


def test_empty_transliteration_is_not_fatal():
    result = LexemeValidator().validate(
        make_lexeme(transliteration="")
    )

    assert result.is_valid
    assert result.error_count == 0


def test_whitespace_transliteration_produces_warning():
    result = LexemeValidator().validate(
        make_lexeme(transliteration="   ")
    )

    assert result.is_valid
    assert result.warning_count == 1

    issue = result.warnings[0]

    assert issue.code == "LEX006"
    assert issue.field == "transliteration"


def test_description_is_optional():
    result = LexemeValidator().validate(
        make_lexeme(description="")
    )

    assert result.is_valid


# =============================================================
# Aliases
# =============================================================


def test_empty_alias_set_is_valid():
    result = LexemeValidator().validate(
        make_lexeme(aliases=frozenset())
    )

    assert result.is_valid


def test_valid_aliases_are_accepted():
    result = LexemeValidator().validate(
        make_lexeme(
            aliases=frozenset(
                {
                    "राम",
                    "rāma",
                }
            )
        )
    )

    assert result.is_valid


# =============================================================
# Multiple errors
# =============================================================


def test_multiple_invalid_required_fields_report_multiple_issues():
    result = LexemeValidator().validate(
        make_lexeme(
            identifier="",
            lemma="",
            language="",
            script="",
        )
    )

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX001" in codes
    assert "LEX002" in codes
    assert "LEX003" in codes
    assert "LEX004" in codes


# =============================================================
# Reusability
# =============================================================


def test_validator_can_be_reused():
    validator = LexemeValidator()

    valid_result = validator.validate(
        make_lexeme()
    )

    invalid_result = validator.validate(
        make_lexeme(identifier="")
    )

    assert valid_result.is_valid
    assert not invalid_result.is_valid


def test_validation_does_not_mutate_lexeme():
    lexeme = make_lexeme(
        aliases=frozenset({"रमा"})
    )

    original = (
        lexeme.identifier,
        lexeme.lemma,
        lexeme.language,
        lexeme.script,
        lexeme.transliteration,
        lexeme.description,
        lexeme.aliases,
    )

    LexemeValidator().validate(lexeme)

    assert (
        lexeme.identifier,
        lexeme.lemma,
        lexeme.language,
        lexeme.script,
        lexeme.transliteration,
        lexeme.description,
        lexeme.aliases,
    ) == original


# =============================================================
# Invalid object
# =============================================================


def test_invalid_object_returns_validation_result():
    result = LexemeValidator().validate(
        object()
    )

    assert isinstance(result, ValidationResult)
    assert not result.is_valid
    assert result.error_count == 1


def test_invalid_object_produces_lex000():
    result = LexemeValidator().validate(
        object()
    )

    assert result.issues[0].code == "LEX000"
