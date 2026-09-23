from __future__ import annotations

"""
SanskritAI
==========

Validation Result

Represents the complete outcome of a validation operation.

A ValidationResult is immutable and contains zero or more
ValidationIssue objects. Multiple validation results may be
merged to produce a consolidated report.

Version
-------
v0.4.0
"""

from dataclasses import dataclass, field, replace
from typing import Iterable

from SanskritAI.core.validators.validation_issue import (
    ValidationIssue,
    ValidationSeverity,
)


@dataclass(slots=True, frozen=True)
class ValidationResult:
    """
    Immutable validation report.
    """

    issues: tuple[ValidationIssue, ...] = field(default_factory=tuple)

    # ---------------------------------------------------------
    # Construction
    # ---------------------------------------------------------

    @classmethod
    def success(cls) -> "ValidationResult":
        """
        Construct a successful validation result.
        """
        return cls()

    @classmethod
    def from_issues(
        cls,
        issues: Iterable[ValidationIssue],
    ) -> "ValidationResult":
        """
        Construct from an iterable of validation issues.
        """
        return cls(tuple(issues))

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    @property
    def is_valid(self) -> bool:
        """
        True if no validation errors are present.
        """
        return not self.has_errors

    @property
    def has_errors(self) -> bool:
        """
        True if at least one error exists.
        """
        return any(issue.is_error for issue in self.issues)

    @property
    def has_warnings(self) -> bool:
        """
        True if at least one warning exists.
        """
        return any(issue.is_warning for issue in self.issues)

    @property
    def has_info(self) -> bool:
        """
        True if at least one informational issue exists.
        """
        return any(issue.is_info for issue in self.issues)

    # ---------------------------------------------------------
    # Counts
    # ---------------------------------------------------------

    @property
    def error_count(self) -> int:
        return sum(
            1
            for issue in self.issues
            if issue.severity == ValidationSeverity.ERROR
        )

    @property
    def warning_count(self) -> int:
        return sum(
            1
            for issue in self.issues
            if issue.severity == ValidationSeverity.WARNING
        )

    @property
    def info_count(self) -> int:
        return sum(
            1
            for issue in self.issues
            if issue.severity == ValidationSeverity.INFO
        )

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(
            issue
            for issue in self.issues
            if issue.severity == ValidationSeverity.ERROR
        )

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(
            issue
            for issue in self.issues
            if issue.severity == ValidationSeverity.WARNING
        )

    @property
    def info(self) -> tuple[ValidationIssue, ...]:
        return tuple(
            issue
            for issue in self.issues
            if issue.severity == ValidationSeverity.INFO
        )

    # ---------------------------------------------------------
    # Composition
    # ---------------------------------------------------------

    def merge(
        self,
        other: "ValidationResult",
    ) -> "ValidationResult":
        """
        Merge two validation results.
        """
        return replace(
            self,
            issues=self.issues + other.issues,
        )

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def __bool__(self) -> bool:
        """
        Truthiness reflects overall validity.
        """
        return self.is_valid

    def __len__(self) -> int:
        """
        Number of validation issues.
        """
        return len(self.issues)
