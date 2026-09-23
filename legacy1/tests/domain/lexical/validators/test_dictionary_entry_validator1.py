
from __future__ import annotations

from SanskritAI.core.validators.validation_result import ValidationResult
from SanskritAI.domain.lexical.dictionary_entry import DictionaryEntry
from SanskritAI.domain.lexical.validators.dictionary_entry_validator import (
    DictionaryEntryValidator,
)


def make_entry(
    *,
    identifier: str = "dictionary-entry-1",
    lemma: str = "धर्म",
    language: str = "Sanskrit",
    source: str = "Test Dictionary",
    transliteration: str = "dharma",
    description: str = "dharma",
    senses: tuple[str, ...] = (),
) -> DictionaryEntry:
    return DictionaryEntry(
        identifier=identifier,
        lemma=lemma,
        language=language,
        source=source,
        transliteration=transliteration,
        description=description,
        senses=senses,
    )


def test_valid_dictionary_entry_passes_validation():
    result = DictionaryEntryValidator().validate(
        make_entry()
    )

    assert isinstance(result, ValidationResult)
    assert result.is_valid
    assert result.error_count == 0


def test_validator_supports_dictionary_entry():
    assert DictionaryEntryValidator.supports(
        make_entry()
    )


def test_validator_rejects_arbitrary_object():
    assert not DictionaryEntryValidator.supports(
        object()
    )


def test_empty_identifier_is_invalid():
    result = DictionaryEntryValidator().validate(
        make_entry(identifier="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DIC002"
        for issue in result.issues
    )


def test_whitespace_identifier_is_invalid():
    result = DictionaryEntryValidator().validate(
        make_entry(identifier="   ")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DIC002"
        for issue in result.issues
    )


def test_empty_lemma_is_invalid():
    result = DictionaryEntryValidator().validate(
        make_entry(lemma="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DIC003"
        for issue in result.issues
    )


def test_whitespace_lemma_is_invalid():
    result = DictionaryEntryValidator().validate(
        make_entry(lemma="   ")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DIC003"
        for issue in result.issues
    )


def test_empty_language_is_invalid():
    result = DictionaryEntryValidator().validate(
        make_entry(language="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DIC004"
        for issue in result.issues
    )


def test_empty_source_produces_warning():
    result = DictionaryEntryValidator().validate(
        make_entry(source="")
    )

    assert result.is_valid
    assert result.warning_count == 1
    assert result.warnings[0].code == "DIC005"


def test_source_is_not_required_for_structural_validity():
    result = DictionaryEntryValidator().validate(
        make_entry(source="")
    )

    assert result.is_valid


def test_empty_transliteration_is_allowed():
    result = DictionaryEntryValidator().validate(
        make_entry(transliteration="")
    )

    assert result.is_valid


def test_empty_description_is_allowed():
    result = DictionaryEntryValidator().validate(
        make_entry(description="")
    )

    assert result.is_valid


def test_empty_senses_are_allowed():
    result = DictionaryEntryValidator().validate(
        make_entry(senses=())
    )

    assert result.is_valid


def test_valid_sense_identifiers_are_accepted():
    result = DictionaryEntryValidator().validate(
        make_entry(
            senses=(
                "sense-1",
                "sense-2",
            )
        )
    )

    assert result.is_valid


def test_multiple_invalid_required_fields_are_reported():
    result = DictionaryEntryValidator().validate(
        make_entry(
            identifier="",
            lemma="",
            language="",
        )
    )

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "DIC002" in codes
    assert "DIC003" in codes
    assert "DIC004" in codes


def test_invalid_object_returns_validation_result():
    result = DictionaryEntryValidator().validate(
        object()
    )

    assert isinstance(result, ValidationResult)
    assert not result.is_valid
    assert result.error_count == 1


def test_invalid_object_produces_dic001():
    result = DictionaryEntryValidator().validate(
        object()
    )

    assert result.issues[0].code == "DIC001"


def test_validator_can_be_reused():
    validator = DictionaryEntryValidator()

    valid = validator.validate(
        make_entry()
    )

    invalid = validator.validate(
        make_entry(identifier="")
    )

    assert valid.is_valid
    assert not invalid.is_valid


def test_dictionary_entry_is_immutable():
    entry = make_entry()

    try:
        entry.lemma = "कर्म"
        mutated = True
    except Exception:
        mutated = False

    assert mutated is False


def test_dictionary_entry_reports_senses():
    entry = make_entry(
        senses=(
            "sense-1",
            "sense-2",
        )
    )

    assert entry.has_senses
    assert entry.sense_count == 2


def test_dictionary_entry_without_senses_reports_no_senses():
    entry = make_entry()

    assert not entry.has_senses
    assert entry.sense_count == 0


def test_validator_does_not_mutate_entry():
    entry = make_entry(
        senses=("sense-1",)
    )

    original = (
        entry.identifier,
        entry.lemma,
        entry.language,
        entry.source,
        entry.transliteration,
        entry.description,
        entry.senses,
    )

    DictionaryEntryValidator().validate(entry)

    assert (
        entry.identifier,
        entry.lemma,
        entry.language,
        entry.source,
        entry.transliteration,
        entry.description,
        entry.senses,
    ) == original
