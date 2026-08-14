from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)
from SanskritAI.lexical.models.dictionary_sense_metadata import (
    DictionarySenseMetadata,
)
from SanskritAI.lexical.validators.dictionary_sense_validator import (
    DictionarySenseValidator,
)


# =============================================================
# Fixtures / Helpers
# =============================================================


def make_metadata(
    *,
    sense_number: int = 1,
    definition: str = "man",
    short_definition: str = "man",
    gloss: str = "person",
) -> DictionarySenseMetadata:
    return DictionarySenseMetadata(
        sense_number=sense_number,
        definition=definition,
        short_definition=short_definition,
        gloss=gloss,
    )


def make_dictionary_sense(
    *,
    identifier: str = "sense-1",
    metadata: DictionarySenseMetadata | None = None,
) -> DictionarySense:
    if metadata is None:
        metadata = make_metadata()

    return DictionarySense(
        identifier=identifier,
        metadata=metadata,
    )


# =============================================================
# Basic Validation
# =============================================================


def test_valid_dictionary_sense_passes_validation():
    sense = make_dictionary_sense()

    result = DictionarySenseValidator().validate(sense)

    assert result.is_valid


def test_valid_dictionary_sense_has_no_validation_errors():
    sense = make_dictionary_sense()

    result = DictionarySenseValidator().validate(sense)

    assert result.errors == ()


def test_valid_dictionary_sense_has_no_issues():
    sense = make_dictionary_sense()

    result = DictionarySenseValidator().validate(sense)

    assert result.issues == ()


# =============================================================
# LEX001 — Identifier
# =============================================================


def test_empty_identifier_produces_lex001():
    sense = make_dictionary_sense(
        identifier="",
    )

    result = DictionarySenseValidator().validate(sense)

    assert not result.is_valid

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX001" in codes


def test_empty_identifier_issue_has_identifier_field():
    sense = make_dictionary_sense(
        identifier="",
    )

    result = DictionarySenseValidator().validate(sense)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert issue.field == "identifier"


def test_empty_identifier_issue_has_message():
    sense = make_dictionary_sense(
        identifier="",
    )

    result = DictionarySenseValidator().validate(sense)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert issue.message == (
        "Dictionary sense identifier must not be empty."
    )


def test_whitespace_identifier_is_not_treated_as_empty():
    sense = make_dictionary_sense(
        identifier="   ",
    )

    result = DictionarySenseValidator().validate(sense)

    assert result.is_valid


# =============================================================
# LEX002 — Metadata
# =============================================================


def test_missing_metadata_produces_lex002():
    sense = make_dictionary_sense()

    sense._metadata = None

    result = DictionarySenseValidator().validate(sense)

    assert not result.is_valid

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX002" in codes


def test_missing_metadata_issue_has_metadata_field():
    sense = make_dictionary_sense()

    sense._metadata = None

    result = DictionarySenseValidator().validate(sense)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert issue.field == "metadata"


def test_missing_metadata_issue_has_message():
    sense = make_dictionary_sense()

    sense._metadata = None

    result = DictionarySenseValidator().validate(sense)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert issue.message == (
        "Dictionary sense metadata is required."
    )


# =============================================================
# Combined Validation
# =============================================================


def test_empty_identifier_and_missing_metadata_report_both_issues():
    sense = make_dictionary_sense(
        identifier="",
    )

    sense._metadata = None

    result = DictionarySenseValidator().validate(sense)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX001" in codes
    assert "LEX002" in codes


def test_all_invalid_conditions_report_all_issues():
    sense = make_dictionary_sense(
        identifier="",
    )

    sense._metadata = None

    result = DictionarySenseValidator().validate(sense)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX001",
        "LEX002",
    }


# =============================================================
# Metadata Values
# =============================================================


def test_validator_accepts_sense_with_metadata_values():
    sense = make_dictionary_sense(
        metadata=DictionarySenseMetadata(
            sense_number=2,
            definition="hero",
            short_definition="heroic person",
            gloss="warrior",
            semantic_domain="person",
            usage_label="literary",
            register="formal",
            grammatical_note="noun",
            etymology="traditional",
            examples=["नरोत्तमः"],
            citations=["example citation"],
            cross_references=["sense-3"],
            notes="editorial note",
        ),
    )

    result = DictionarySenseValidator().validate(sense)

    assert result.is_valid


def test_metadata_object_itself_is_not_validated_for_empty_definition():
    sense = make_dictionary_sense(
        metadata=DictionarySenseMetadata(
            definition="",
        ),
    )

    result = DictionarySenseValidator().validate(sense)

    assert result.is_valid


def test_metadata_object_itself_is_not_validated_for_empty_gloss():
    sense = make_dictionary_sense(
        metadata=DictionarySenseMetadata(
            gloss="",
        ),
    )

    result = DictionarySenseValidator().validate(sense)

    assert result.is_valid


# =============================================================
# Validator Reuse
# =============================================================


def test_validator_can_be_reused():
    validator = DictionarySenseValidator()

    valid = validator.validate(
        make_dictionary_sense()
    )

    invalid = validator.validate(
        make_dictionary_sense(
            identifier="",
        )
    )

    assert valid.is_valid
    assert not invalid.is_valid


def test_validator_does_not_retain_previous_issues():
    validator = DictionarySenseValidator()

    invalid = validator.validate(
        make_dictionary_sense(
            identifier="",
        )
    )

    valid = validator.validate(
        make_dictionary_sense()
    )

    assert not invalid.is_valid
    assert valid.is_valid
    assert valid.issues == ()


# =============================================================
# Result Contract
# =============================================================


def test_valid_result_contains_no_errors():
    sense = make_dictionary_sense()

    result = DictionarySenseValidator().validate(sense)

    assert result.errors == ()


def test_invalid_result_contains_errors():
    sense = make_dictionary_sense(
        identifier="",
    )

    result = DictionarySenseValidator().validate(sense)

    assert result.errors
    assert any(
        issue.code == "LEX001"
        for issue in result.errors
    )
