import pytest

from SanskritAI.core.validators.validation_issue import (
    ValidationIssue,
    ValidationSeverity,
)


def test_validation_severity_defines_expected_values():
    assert ValidationSeverity.INFO.value == "info"
    assert ValidationSeverity.WARNING.value == "warning"
    assert ValidationSeverity.ERROR.value == "error"


def test_validation_severity_is_string_enum():
    assert isinstance(ValidationSeverity.INFO, str)
    assert isinstance(ValidationSeverity.WARNING, str)
    assert isinstance(ValidationSeverity.ERROR, str)


def test_validation_issue_can_be_created_with_required_fields():
    issue = ValidationIssue(
        code="LEX001",
        message="Invalid lexical identifier.",
    )

    assert issue.code == "LEX001"
    assert issue.message == "Invalid lexical identifier."


def test_validation_issue_defaults_to_error():
    issue = ValidationIssue(
        code="LEX001",
        message="Invalid lexical identifier.",
    )

    assert issue.severity == ValidationSeverity.ERROR
    assert issue.is_error is True
    assert issue.is_warning is False
    assert issue.is_info is False


def test_validation_issue_accepts_warning():
    issue = ValidationIssue(
        code="LEX002",
        message="Lemma is deprecated.",
        severity=ValidationSeverity.WARNING,
    )

    assert issue.severity == ValidationSeverity.WARNING
    assert issue.is_warning is True
    assert issue.is_error is False
    assert issue.is_info is False


def test_validation_issue_accepts_info():
    issue = ValidationIssue(
        code="LEX003",
        message="Additional lexical information is available.",
        severity=ValidationSeverity.INFO,
    )

    assert issue.severity == ValidationSeverity.INFO
    assert issue.is_info is True
    assert issue.is_error is False
    assert issue.is_warning is False


def test_validation_issue_supports_field():
    issue = ValidationIssue(
        code="LEX004",
        message="Lemma is required.",
        field="lemma",
    )

    assert issue.field == "lemma"


def test_validation_issue_supports_location():
    issue = ValidationIssue(
        code="LEX005",
        message="Invalid value.",
        location="dictionary_entry.metadata.lemma",
    )

    assert issue.location == "dictionary_entry.metadata.lemma"


def test_validation_issue_supports_suggestion():
    issue = ValidationIssue(
        code="LEX006",
        message="Lemma is missing.",
        suggestion="Provide the canonical lemma.",
    )

    assert issue.suggestion == "Provide the canonical lemma."


def test_validation_issue_optional_fields_default_to_empty_strings():
    issue = ValidationIssue(
        code="LEX007",
        message="Validation issue.",
    )

    assert issue.field == ""
    assert issue.location == ""
    assert issue.suggestion == ""


def test_validation_issue_is_frozen():
    issue = ValidationIssue(
        code="LEX008",
        message="Immutable issue.",
    )

    with pytest.raises((AttributeError, TypeError)):
        issue.code = "CHANGED"


def test_validation_issue_is_hashable():
    issue = ValidationIssue(
        code="LEX009",
        message="Hashable issue.",
    )

    assert hash(issue) is not None


def test_validation_issues_with_same_values_are_equal():
    first = ValidationIssue(
        code="LEX010",
        message="Same issue.",
        severity=ValidationSeverity.ERROR,
        field="lemma",
        location="entry.lemma",
        suggestion="Provide a lemma.",
    )

    second = ValidationIssue(
        code="LEX010",
        message="Same issue.",
        severity=ValidationSeverity.ERROR,
        field="lemma",
        location="entry.lemma",
        suggestion="Provide a lemma.",
    )

    assert first == second


def test_validation_issues_with_different_codes_are_not_equal():
    first = ValidationIssue(
        code="LEX011",
        message="Validation issue.",
    )

    second = ValidationIssue(
        code="LEX012",
        message="Validation issue.",
    )

    assert first != second


def test_validation_issue_severity_predicates_are_mutually_consistent():
    issues = (
        ValidationIssue(
            code="INFO",
            message="Information.",
            severity=ValidationSeverity.INFO,
        ),
        ValidationIssue(
            code="WARNING",
            message="Warning.",
            severity=ValidationSeverity.WARNING,
        ),
        ValidationIssue(
            code="ERROR",
            message="Error.",
            severity=ValidationSeverity.ERROR,
        ),
    )

    assert sum(issue.is_info for issue in issues) == 1
    assert sum(issue.is_warning for issue in issues) == 1
    assert sum(issue.is_error for issue in issues) == 1
