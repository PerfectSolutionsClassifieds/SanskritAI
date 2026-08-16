
from __future__ import annotations

"""
SanskritAI
==========

Base Lexical Validator
----------------------

Provides reusable validation helpers for lexical-domain validators.

This class deliberately contains no model-specific validation rules.
Concrete validators such as LexemeValidator, DictionaryEntryValidator,
DictionarySenseValidator, LexicalRelationValidator, and
LexicalSourceValidator are responsible for their own domain rules.

The validator returns immutable ValidationResult instances through the
core validation infrastructure.
"""

from abc import abstractmethod
from typing import Generic, TypeVar

from SanskritAI.core.validators.validation_issue import (
    ValidationIssue,
    ValidationSeverity,
)
from SanskritAI.core.validators.validation_result import ValidationResult
from SanskritAI.core.validators.validator import Validator


TLexical = TypeVar("TLexical")


class BaseLexicalValidator(
    Validator[TLexical],
    Generic[TLexical],
):
    """
    Base class for validators belonging to the lexical domain.

    The class provides small, reusable helpers for constructing
    ValidationIssue objects and ValidationResult objects.

    Domain-specific validation logic belongs in concrete subclasses.
    """

    # =========================================================
    # Public contract
    # =========================================================

    @abstractmethod
    def validate(
        self,
        obj: TLexical,
    ) -> ValidationResult:
        """
        Validate one lexical-domain object.
        """
        raise NotImplementedError

    # =========================================================
    # Result helpers
    # =========================================================

    @staticmethod
    def success() -> ValidationResult:
        """
        Return a successful validation result.
        """
        return ValidationResult.success()

    @staticmethod
    def result_from_issues(
        *issues: ValidationIssue,
    ) -> ValidationResult:
        """
        Construct a ValidationResult from the supplied issues.
        """
        return ValidationResult.from_issues(issues)

    # =========================================================
    # Issue helpers
    # =========================================================

    @staticmethod
    def error(
        *,
        code: str,
        message: str,
        field: str = "",
        location: str = "",
        suggestion: str = "",
    ) -> ValidationIssue:
        """
        Construct an error-level validation issue.
        """
        return ValidationIssue(
            code=code,
            message=message,
            severity=ValidationSeverity.ERROR,
            field=field,
            location=location,
            suggestion=suggestion,
        )

    @staticmethod
    def warning(
        *,
        code: str,
        message: str,
        field: str = "",
        location: str = "",
        suggestion: str = "",
    ) -> ValidationIssue:
        """
        Construct a warning-level validation issue.
        """
        return ValidationIssue(
            code=code,
            message=message,
            severity=ValidationSeverity.WARNING,
            field=field,
            location=location,
            suggestion=suggestion,
        )

    @staticmethod
    def info(
        *,
        code: str,
        message: str,
        field: str = "",
        location: str = "",
        suggestion: str = "",
    ) -> ValidationIssue:
        """
        Construct an informational validation issue.
        """
        return ValidationIssue(
            code=code,
            message=message,
            severity=ValidationSeverity.INFO,
            field=field,
            location=location,
            suggestion=suggestion,
        )

    # =========================================================
    # Common lexical checks
    # =========================================================

    @staticmethod
    def is_blank(value: object) -> bool:
        """
        Return True when a value is None or a whitespace-only string.

        Non-string values are considered non-blank here. Type-specific
        validators should report incorrect types when necessary.
        """
        if value is None:
            return True

        if isinstance(value, str):
            return not value.strip()

        return False

    @staticmethod
    def text_error(
        *,
        code: str,
        field: str,
        label: str,
    ) -> ValidationIssue:
        """
        Construct the standard issue for a required textual field.
        """
        return BaseLexicalValidator.error(
            code=code,
            field=field,
            message=f"{label} must not be empty.",
            suggestion=f"Provide a non-empty {label.lower()}.",
        )
