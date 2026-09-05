
from __future__ import annotations

from SanskritAI.core.validators.validation_result import ValidationResult
from SanskritAI.domain.lexical.dictionary_sense import DictionarySense
from SanskritAI.domain.lexical.validators.dictionary_sense_validator import (
    DictionarySenseValidator,
)


def make_sense(
    *,
    identifier: str = "sense-1",
    entry_id: str = "dictionary-entry-1",
    meaning: str = "righteousness",
    language: str = "sanskrit",
    source: str = "Test Dictionary",
    transliteration: str = "dharma",
    grammatical_label: str = "noun",
    usage: str = "general",
    examples: tuple[str, ...] = (),
) -> DictionarySense:
    return DictionarySense(
        identifier=identifier,
        entry_id=entry_id,
        meaning=meaning,
        language=language,
        source=source,
        transliteration=transliteration,
        grammatical_label=grammatical_label,
        usage=usage,
        examples=examples,
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


def test_empty_entry_id_is_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(entry_id="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS003"
        for issue in result.issues
    )


def test_whitespace_entry_id_is_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(entry_id="   ")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS003"
        for issue in result.issues
    )


def test_empty_meaning_is_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(meaning="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS004"
        for issue in result.issues
    )


def test_whitespace_meaning_is_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(meaning="   ")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS004"
        for issue in result.issues
    )


def test_empty_language_is_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(language="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DS005"
        for issue in result.issues
    )


def test_empty_source_produces_warning():
    result = DictionarySenseValidator().validate(
        make_sense(source="")
    )

    assert result.is_valid
    assert result.warning_count == 1
    assert result.warnings[0].code == "DS006"


def test_empty_source_does_not_make_sense_invalid():
    result = DictionarySenseValidator().validate(
        make_sense(source="")
    )

    assert result.is_valid


def test_empty_transliteration_is_allowed():
    result = DictionarySenseValidator().validate(
        make_sense(transliteration="")
    )

    assert result.is_valid


def test_empty_grammatical_label_is_allowed():
    result = DictionarySenseValidator().validate(
        make_sense(grammatical_label="")
    )

    assert result.is_valid


def test_empty_usage_is_allowed():
    result = DictionarySenseValidator().validate(
        make_sense(usage="")
    )

    assert result.is_valid


def test_empty_examples_are_allowed():
    result = DictionarySenseValidator().validate(
        make_sense(examples=())
    )

    assert result.is_valid


def test_valid_examples_are_accepted():
    result = DictionarySenseValidator().validate(
        make_sense(
            examples=(
                "धर्मं चर",
                "धर्म एव हतो हन्ति",
            )
        )
    )

    assert result.is_valid


def test_multiple_required_fields_are_reported():
    result = DictionarySenseValidator().validate(
        make_sense(
            identifier="",
            entry_id="",
            meaning="",
            language="",
        )
    )

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "DS002" in codes
    assert "DS003" in codes
    assert "DS004" in codes
    assert "DS005" in codes


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
        make_sense(meaning="")
    )

    assert valid.is_valid
    assert not invalid.is_valid


def test_dictionary_sense_is_immutable():
    sense = make_sense()

    try:
        sense.meaning = "new meaning"
        mutated = True
    except Exception:
        mutated = False

    assert mutated is False


def test_dictionary_sense_reports_examples():
    sense = make_sense(
        examples=(
            "example-1",
            "example-2",
        )
    )

    assert sense.has_examples
    assert sense.example_count == 2


def test_dictionary_sense_without_examples_reports_no_examples():
    sense = make_sense()

    assert not sense.has_examples
    assert sense.example_count == 0


def test_dictionary_sense_reports_source():
    sense = make_sense(
        source="Monier-Williams"
    )

    assert sense.has_source


def test_dictionary_sense_reports_grammatical_label():
    sense = make_sense(
        grammatical_label="noun"
    )

    assert sense.has_grammatical_label


def test_dictionary_sense_reports_transliteration():
    sense = make_sense(
        transliteration="dharma"
    )

    assert sense.has_transliteration


def test_dictionary_sense_display_name_is_meaning():
    sense = make_sense(
        meaning="righteousness"
    )

    assert sense.display_name == "righteousness"


def test_dictionary_sense_display_text_uses_transliteration():
    sense = make_sense(
        meaning="धर्म",
        transliteration="dharma",
    )

    assert sense.display_text == "धर्म (dharma)"


def test_dictionary_sense_string_uses_display_text():
    sense = make_sense(
        meaning="धर्म",
        transliteration="dharma",
    )

    assert str(sense) == "धर्म (dharma)"
