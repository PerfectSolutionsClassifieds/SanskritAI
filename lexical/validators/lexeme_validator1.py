from __future__ import annotations

"""
SanskritAI
==========

Lexeme Validator

Validates Lexeme domain objects.

Version
-------
v0.4.0
"""

from SanskritAI.core.validators.validation_issue import (
    ValidationIssue,
)
from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)

from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class LexemeValidator(
    BaseLexicalValidator[Lexeme],
):
    """
    Validator for Lexeme objects.
    """

    def validate(
        self,
        obj: Lexeme,
    ) -> ValidationResult:

        issues: list[ValidationIssue] = []

        if not obj.identifier:
            issues.append(
                ValidationIssue(
                    code="LEX001",
                    message="Lexeme identifier must not be empty.",
                    field="identifier",
                )
            )

        if obj.metadata is None:
            issues.append(
                ValidationIssue(
                    code="LEX002",
                    message="Lexeme metadata is required.",
                    field="metadata",
                )
            )

        return ValidationResult.from_issues(issues)
