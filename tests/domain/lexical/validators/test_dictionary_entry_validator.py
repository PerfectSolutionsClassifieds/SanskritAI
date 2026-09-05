
from __future__ import annotations

from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.domain.lexical.validators.dictionary_entry_validator import (
    DictionaryEntryValidator,
)
from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)
from SanskritAI.lexical.models.dictionary_entry_metadata import (
    DictionaryEntryMetadata,
)
from SanskritAI.lexical.models.lexical_source import (
    LexicalSource,
)


def make_entry(
    *,
    identifier: str = "dictionary-entry-1",
    headword: str = "धर्म",
    lemma: str = "धर्म",
    language: str = "sa",
    dictionary_name: str = "Test Dictionary",
    transliteration: str = "dharma",
) -> DictionaryEntry:

    metadata = DictionaryEntryMetadata(
        headword=headword,
        lemma=lemma,
        language=language,
        dictionary_name=dictionary_name,
        transliteration=transliteration,
        entry_identifier=identifier,
    )

    source = LexicalSource(
        identifier="test-dictionary",
        name="Test Dictionary",
    )

    return DictionaryEntry(
        identifier=identifier,
        metadata=metadata,
        source=source,
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


def test_empty_headword_is_invalid():
    result = DictionaryEntryValidator().validate(
        make_entry(headword="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DIC003"
        for issue in result.issues
    )


def test_empty_lemma_is_invalid():
    result = DictionaryEntryValidator().validate(
        make_entry(lemma="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DIC004"
        for issue in result.issues
    )


def test_empty_language_is_invalid():
    result = DictionaryEntryValidator().validate(
        make_entry(language="")
    )

    assert not result.is_valid
    assert any(
        issue.code == "DIC005"
        for issue in result.issues
    )


def test_empty_dictionary_name_produces_warning():
    result = DictionaryEntryValidator().validate(
        make_entry(dictionary_name="")
    )

    assert result.is_valid
    assert result.warning_count == 1
    assert result.warnings[0].code == "DIC006"


def test_empty_transliteration_is_allowed():
    result = DictionaryEntryValidator().validate(
        make_entry(transliteration="")
    )

    assert result.is_valid


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
        entry.identifier = "changed"
        mutated = True
    except Exception:
        mutated = False

    assert mutated is False


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
