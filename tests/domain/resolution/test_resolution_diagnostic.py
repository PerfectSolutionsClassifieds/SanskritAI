
from dataclasses import FrozenInstanceError

import pytest

from SanskritAI.domain.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)


def make_diagnostic(**overrides):
    values = {
        "code": "LEX001",
        "message": "Lexical resolution completed.",
    }
    values.update(overrides)
    return ResolutionDiagnostic(**values)


def test_diagnostic_can_be_created_with_required_fields():
    diagnostic = make_diagnostic()

    assert diagnostic.code == "LEX001"
    assert (
        diagnostic.message
        == "Lexical resolution completed."
    )


def test_default_values():
    diagnostic = make_diagnostic()

    assert diagnostic.severity == "information"
    assert diagnostic.source == ""
    assert diagnostic.recoverable is True


def test_identifier_is_code():
    diagnostic = make_diagnostic(
        code="RES001",
    )

    assert diagnostic.identifier == "RES001"


def test_display_name_is_code():
    diagnostic = make_diagnostic(
        code="RES001",
    )

    assert diagnostic.display_name == "RES001"


def test_display_text_contains_uppercase_severity_and_message():
    diagnostic = make_diagnostic(
        severity="warning",
        message="Ambiguous lexical candidate.",
    )

    assert (
        diagnostic.display_text
        == "[WARNING] Ambiguous lexical candidate."
    )


def test_display_description_is_message():
    diagnostic = make_diagnostic(
        message="Resolution failed.",
    )

    assert diagnostic.display_description == "Resolution failed."


def test_information_severity():
    diagnostic = make_diagnostic(
        severity="information",
    )

    assert diagnostic.is_information
    assert not diagnostic.is_warning
    assert not diagnostic.is_error


def test_warning_severity():
    diagnostic = make_diagnostic(
        severity="warning",
    )

    assert diagnostic.is_warning
    assert not diagnostic.is_information
    assert not diagnostic.is_error


def test_error_severity():
    diagnostic = make_diagnostic(
        severity="error",
    )

    assert diagnostic.is_error
    assert not diagnostic.is_information
    assert not diagnostic.is_warning


def test_severity_checks_are_case_insensitive():
    diagnostic = make_diagnostic(
        severity="WARNING",
    )

    assert diagnostic.is_warning


def test_recoverable_error_is_not_fatal():
    diagnostic = make_diagnostic(
        severity="error",
        recoverable=True,
    )

    assert diagnostic.is_error
    assert not diagnostic.is_fatal


def test_nonrecoverable_error_is_fatal():
    diagnostic = make_diagnostic(
        severity="error",
        recoverable=False,
    )

    assert diagnostic.is_error
    assert diagnostic.is_fatal


def test_non_error_is_never_fatal():
    diagnostic = make_diagnostic(
        severity="warning",
        recoverable=False,
    )

    assert not diagnostic.is_fatal


def test_source_flag():
    diagnostic = make_diagnostic(
        source="lexical",
    )

    assert diagnostic.has_source


def test_empty_source_flag():
    diagnostic = make_diagnostic()

    assert not diagnostic.has_source


def test_diagnostic_is_immutable():
    diagnostic = make_diagnostic()

    with pytest.raises(FrozenInstanceError):
        diagnostic.message = "changed"


def test_diagnostic_is_slot_based():
    diagnostic = make_diagnostic()

    assert not hasattr(diagnostic, "__dict__")


def test_diagnostic_is_immutable_and_displayable():
    diagnostic = make_diagnostic()

    assert diagnostic.is_immutable is True
    assert diagnostic.is_displayable is True


def test_string_representation_uses_display_text():
    diagnostic = make_diagnostic(
        severity="error",
        message="Resolution failed.",
    )

    assert str(diagnostic) == "[ERROR] Resolution failed."
