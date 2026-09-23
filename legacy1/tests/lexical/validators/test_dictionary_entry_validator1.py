from __future__ import annotations

from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)
from SanskritAI.lexical.models.dictionary_entry_metadata import (
    DictionaryEntryMetadata,
)
from SanskritAI.lexical.models.lexical_source import (
    LexicalSource,
)
from SanskritAI.lexical.validators.dictionary_entry_validator import (
    DictionaryEntryValidator,
)


def make_source():
    return LexicalSource(
        identifier="mw",
        name="Monier-Williams",
    )


def make_metadata():
    return DictionaryEntryMetadata(
        lemma="राम",
    )


def make_dictionary_entry(
    identifier: str = "entry-1",
    source=None,
    metadata=None,
):
    if source is None:
        source = make_source()

    if metadata is None:
        metadata = make_metadata()

    return DictionaryEntry(
        identifier=identifier,
        source=source,
        metadata=metadata,
    )


# =============================================================
# Valid Entry
# =============================================================


def test_valid_dictionary_entry_passes_validation():
    entry = make_dictionary_entry()

    result = DictionaryEntryValidator().validate(entry)

    assert result.is_valid


def test_valid_dictionary_entry_has_no_errors():
    entry = make_dictionary_entry()

    result = DictionaryEntryValidator().validate(entry)

    assert result.errors == ()


# =============================================================
# LEX001 — Identifier
# =============================================================


def test_empty_identifier_produces_lex001():
    entry = make_dictionary_entry(identifier="")

    result = DictionaryEntryValidator().validate(entry)

    assert not result.is_valid
    assert any(
        issue.code == "LEX001"
        for issue in result.issues
    )


def test_empty_identifier_issue_has_identifier_field():
    entry = make_dictionary_entry(identifier="")

    result = DictionaryEntryValidator().validate(entry)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert issue.field == "identifier"


def test_empty_identifier_issue_has_message():
    entry = make_dictionary_entry(identifier="")

    result = DictionaryEntryValidator().validate(entry)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX001"
    )

    assert "identifier" in issue.message.lower()


# =============================================================
# LEX002 — Source
# =============================================================


def test_missing_source_produces_lex002():
    entry = make_dictionary_entry(
        source=None,
    )

    result = DictionaryEntryValidator().validate(entry)

    assert not result.is_valid
    assert any(
        issue.code == "LEX002"
        for issue in result.issues
    )


def test_missing_source_issue_has_source_field():
    entry = make_dictionary_entry(
        source=None,
    )

    result = DictionaryEntryValidator().validate(entry)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert issue.field == "source"


def test_missing_source_issue_has_message():
    entry = make_dictionary_entry(
        source=None,
    )

    result = DictionaryEntryValidator().validate(entry)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX002"
    )

    assert "source" in issue.message.lower()


# =============================================================
# LEX003 — Metadata
# =============================================================


def test_missing_metadata_produces_lex003():
    entry = make_dictionary_entry()
    entry._metadata = None

    result = DictionaryEntryValidator().validate(entry)

    assert not result.is_valid
    assert any(
        issue.code == "LEX003"
        for issue in result.issues
    )


def test_missing_metadata_issue_has_metadata_field():
    entry = make_dictionary_entry()
    entry._metadata = None

    result = DictionaryEntryValidator().validate(entry)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX003"
    )

    assert issue.field == "metadata"


def test_missing_metadata_issue_has_message():
    entry = make_dictionary_entry()
    entry._metadata = None

    result = DictionaryEntryValidator().validate(entry)

    issue = next(
        issue
        for issue in result.issues
        if issue.code == "LEX003"
    )

    assert "metadata" in issue.message.lower()


# =============================================================
# Multiple Issues
# =============================================================


def test_empty_identifier_and_missing_metadata_report_both():
    entry = make_dictionary_entry(
        identifier="",
    )
    entry._metadata = None

    result = DictionaryEntryValidator().validate(entry)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX001" in codes
    assert "LEX003" in codes


def test_empty_identifier_and_missing_source_report_both():
    entry = make_dictionary_entry(
        identifier="",
        source=None,
    )

    result = DictionaryEntryValidator().validate(entry)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX001" in codes
    assert "LEX002" in codes


def test_missing_source_and_metadata_report_both():
    entry = make_dictionary_entry(
        source=None,
    )
    entry._metadata = None

    result = DictionaryEntryValidator().validate(entry)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert "LEX002" in codes
    assert "LEX003" in codes


def test_all_invalid_conditions_report_all_issues():
    entry = make_dictionary_entry(
        identifier="",
        source=None,
    )
    entry._metadata = None

    result = DictionaryEntryValidator().validate(entry)

    codes = {
        issue.code
        for issue in result.issues
    }

    assert codes == {
        "LEX001",
        "LEX002",
        "LEX003",
    }


# =============================================================
# Reusability
# =============================================================


def test_validator_can_be_reused():
    validator = DictionaryEntryValidator()

    valid = validator.validate(
        make_dictionary_entry()
    )

    invalid = validator.validate(
        make_dictionary_entry(identifier="")
    )

    assert valid.is_valid
    assert not invalid.is_valid


def test_validator_does_not_retain_previous_issues():
    validator = DictionaryEntryValidator()

    invalid = validator.validate(
        make_dictionary_entry(identifier="")
    )

    valid = validator.validate(
        make_dictionary_entry()
    )

    assert not invalid.is_valid
    assert valid.is_valid
    assert valid.issues == ()
