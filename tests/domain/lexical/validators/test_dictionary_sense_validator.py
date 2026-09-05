
from __future__ import annotations

from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.domain.lexical.validators.dictionary_sense_validator import (
    DictionarySenseValidator,
)
from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)
from SanskritAI.lexical.models.dictionary_sense_metadata import (
    DictionarySenseMetadata,
)


def make_sense(
    *,
    identifier: str = "sense-1",
    definition: str = "righteousness",
    language: str = "en",
    transliteration: str = "dharma",
    grammatical_note: str = "noun",
    examples: list[str] | None = None,
) -> DictionarySense:

    metadata = DictionarySenseMetadata(
        sense_number=1,
        definition=definition,
        language=language,
        transliteration=transliteration,
        grammatical_note=grammatical_note,
        examples=(
            [] if examples is None else examples
        ),
    )

    return DictionarySense(
        identifier=identifier,
        metadata=metadata,
    )


def test_valid_dictionary_sense_passes_validation():
    result = DictionarySenseValidator().validate(
        make_sense()
    )

    assert isinstance(result, ValidationResult)
    assert result.is_valid
    assert result.error_count == 0


def test_validator_supports_dictionary_sense():
    assert DictionarySenseValidator.supports(
        make_sense()
    )


def test_validator_rejects_arbitrary_object():
    assert not DictionarySenseValidator.supports(
        object()
    )


def test_empty_identifier_is_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(identifier="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS002"
        for issue in result.issues
    )


def test_whitespace_identifier_is_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(identifier="   ")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS002"
        for issue in result.issues
    )


def test_empty_definition_is_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(definition="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS003"
        for issue in result.issues
    )


def test_empty_language_is_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(language="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS004"
        for issue in result.issues
    )


def test_empty_optional_fields_are_allowed():
    result = DictionarySenseValidator().validate(
        make_sense(
            transliteration="",
            grammatical_note="",
        )
    )

    assert result.is_valid


def test_sense_number_must_be_positive():
    metadata = DictionarySenseMetadata(
        sense_number=0,
        definition="meaning",
        language="en",
    )

    sense = DictionarySense(
        identifier="sense-1",
        metadata=metadata,
    )

    result = DictionarySenseValidator().validate(
        sense
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS006"
        for issue in result.issues
    )


def test_valid_examples_are_accepted():
    result = DictionarySenseValidator().validate(
        make_sense(
            examples=[
                "धर्मं चर",
                "धर्म एव हतो हन्ति",
            ]
        )
    )

    assert result.is_valid


def test_dictionary_sense_is_immutable():
    sense = make_sense()

    try:
        sense.identifier = "changed"
        mutated = True
    except Exception:
        mutated = False

    assert mutated is False


def test_dictionary_sense_reports_definition():
    sense = make_sense(
        definition="righteousness"
    )

    assert sense.definition == "righteousness"


def test_dictionary_sense_reports_examples():
    sense = make_sense(
        examples=[
            "example-1",
            "example-2",
        ]
    )

    assert sense.examples == [
        "example-1",
        "example-2",
    ]


def test_dictionary_sense_reports_transliteration():
    sense = make_sense(
        transliteration="dharma"
    )

    assert sense.metadata.transliteration == "dharma"


def test_dictionary_sense_reports_grammatical_note():
    sense = make_sense(
        grammatical_note="noun"
    )

    assert sense.grammatical_note == "noun"


def test_invalid_object_returns_validation_result():
    result = DictionarySenseValidator().validate(
        object()
    )

    assert isinstance(result, ValidationResult)
    assert not result.is_valid
    assert result.error_count == 1


def test_invalid_object_produces_ds001():
    result = DictionarySenseValidator().validate(
        object()
    )

    assert result.issues[0].code == "DS001"


def test_validator_can_be_reused():
    validator = DictionarySenseValidator()

    valid = validator.validate(
        make_sense()
    )

    invalid = validator.validate(
        make_sense(definition="")
    )

    assert valid.is_valid
    assert not invalid.is_valid
