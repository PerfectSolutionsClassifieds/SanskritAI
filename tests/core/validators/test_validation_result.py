import pytest

from SanskritAI.core.validators.validation_issue import (
    ValidationIssue,
    ValidationSeverity,
)
from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)


def make_info_issue() -> ValidationIssue:
    return ValidationIssue(
        code="INFO001",
        message="Informational message.",
        severity=ValidationSeverity.INFO,
    )


def make_warning_issue() -> ValidationIssue:
    return ValidationIssue(
        code="WARN001",
        message="Warning message.",
        severity=ValidationSeverity.WARNING,
    )


def make_error_issue() -> ValidationIssue:
    return ValidationIssue(
        code="ERR001",
        message="Error message.",
        severity=ValidationSeverity.ERROR,
    )


# =============================================================
# Construction
# =============================================================


def test_default_result_is_successful():
    result = ValidationResult()

    assert result.issues == ()
    assert result.is_valid is True


def test_success_creates_empty_result():
    result = ValidationResult.success()

    assert result.issues == ()
    assert result.is_valid is True
    assert len(result) == 0


def test_from_issues_accepts_iterable():
    issues = [
        make_warning_issue(),
        make_error_issue(),
    ]

    result = ValidationResult.from_issues(issues)

    assert result.issues == tuple(issues)


def test_from_issues_accepts_generator():
    result = ValidationResult.from_issues(
        issue
        for issue in (
            make_info_issue(),
            make_warning_issue(),
        )
    )

    assert len(result) == 2


# =============================================================
# Status
# =============================================================


def test_result_with_info_only_is_valid():
    result = ValidationResult.from_issues(
        [make_info_issue()]
    )

    assert result.is_valid is True
    assert result.has_errors is False
    assert result.has_info is True
    assert result.has_warnings is False


def test_result_with_warning_only_is_valid():
    result = ValidationResult.from_issues(
        [make_warning_issue()]
    )

    assert result.is_valid is True
    assert result.has_errors is False
    assert result.has_warnings is True


def test_result_with_error_is_invalid():
    result = ValidationResult.from_issues(
        [make_error_issue()]
    )

    assert result.is_valid is False
    assert result.has_errors is True


def test_result_detects_all_severities():
    result = ValidationResult.from_issues(
        [
            make_info_issue(),
            make_warning_issue(),
            make_error_issue(),
        ]
    )

    assert result.has_info is True
    assert result.has_warnings is True
    assert result.has_errors is True
    assert result.is_valid is False


# =============================================================
# Counts
# =============================================================


def test_error_count():
    result = ValidationResult.from_issues(
        [
            make_error_issue(),
            make_error_issue(),
            make_warning_issue(),
        ]
    )

    assert result.error_count == 2


def test_warning_count():
    result = ValidationResult.from_issues(
        [
            make_warning_issue(),
            make_warning_issue(),
            make_error_issue(),
        ]
    )

    assert result.warning_count == 2


def test_info_count():
    result = ValidationResult.from_issues(
        [
            make_info_issue(),
            make_info_issue(),
            make_error_issue(),
        ]
    )

    assert result.info_count == 2


def test_counts_are_zero_when_no_matching_issue_exists():
    result = ValidationResult.from_issues(
        [make_error_issue()]
    )

    assert result.warning_count == 0
    assert result.info_count == 0


# =============================================================
# Filtering
# =============================================================


def test_errors_returns_only_errors():
    error = make_error_issue()

    result = ValidationResult.from_issues(
        [
            make_info_issue(),
            make_warning_issue(),
            error,
        ]
    )

    assert result.errors == (error,)


def test_warnings_returns_only_warnings():
    warning = make_warning_issue()

    result = ValidationResult.from_issues(
        [
            make_info_issue(),
            warning,
            make_error_issue(),
        ]
    )

    assert result.warnings == (warning,)


def test_info_returns_only_info_issues():
    info = make_info_issue()

    result = ValidationResult.from_issues(
        [
            info,
            make_warning_issue(),
            make_error_issue(),
        ]
    )

    assert result.info == (info,)


def test_filtering_preserves_original_order():
    first = ValidationIssue(
        code="ERR001",
        message="First error.",
        severity=ValidationSeverity.ERROR,
    )
    second = ValidationIssue(
        code="ERR002",
        message="Second error.",
        severity=ValidationSeverity.ERROR,
    )

    result = ValidationResult.from_issues(
        [
            first,
            make_warning_issue(),
            second,
        ]
    )

    assert result.errors == (first, second)


# =============================================================
# Composition
# =============================================================


def test_merge_combines_issues():
    first = ValidationResult.from_issues(
        [make_error_issue()]
    )
    second = ValidationResult.from_issues(
        [make_warning_issue()]
    )

    merged = first.merge(second)

    assert len(merged) == 2
    assert merged.issues == (
        make_error_issue(),
        make_warning_issue(),
    )


def test_merge_preserves_order():
    first_issue = make_info_issue()
    second_issue = make_error_issue()

    first = ValidationResult.from_issues([first_issue])
    second = ValidationResult.from_issues([second_issue])

    merged = first.merge(second)

    assert merged.issues == (
        first_issue,
        second_issue,
    )


def test_merge_does_not_modify_original_results():
    first = ValidationResult.from_issues(
        [make_error_issue()]
    )
    second = ValidationResult.from_issues(
        [make_warning_issue()]
    )

    merged = first.merge(second)

    assert len(first) == 1
    assert len(second) == 1
    assert len(merged) == 2


# =============================================================
# Convenience
# =============================================================


def test_bool_is_true_for_valid_result():
    result = ValidationResult.from_issues(
        [make_warning_issue()]
    )

    assert bool(result) is True


def test_bool_is_false_for_invalid_result():
    result = ValidationResult.from_issues(
        [make_error_issue()]
    )

    assert bool(result) is False


def test_len_returns_number_of_issues():
    result = ValidationResult.from_issues(
        [
            make_info_issue(),
            make_warning_issue(),
            make_error_issue(),
        ]
    )

    assert len(result) == 3


# =============================================================
# Immutability
# =============================================================


def test_validation_result_is_frozen():
    result = ValidationResult.success()

    with pytest.raises((AttributeError, TypeError)):
        result.issues = (make_error_issue(),)


def test_issues_are_stored_as_tuple():
    result = ValidationResult.from_issues(
        [
            make_info_issue(),
            make_warning_issue(),
        ]
    )

    assert isinstance(result.issues, tuple)


# =============================================================
# Equality
# =============================================================


def test_equal_results_are_equal():
    first = ValidationResult.from_issues(
        [make_error_issue()]
    )
    second = ValidationResult.from_issues(
        [make_error_issue()]
    )

    assert first == second


def test_results_with_different_issues_are_not_equal():
    first = ValidationResult.from_issues(
        [make_error_issue()]
    )
    second = ValidationResult.from_issues(
        [make_warning_issue()]
    )

    assert first != second
