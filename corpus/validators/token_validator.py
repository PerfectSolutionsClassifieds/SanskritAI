from __future__ import annotations

"""
SanskritAI
==========

Token Validator

Validates Token objects.

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
from SanskritAI.corpus.models.token import Token
from SanskritAI.corpus.validators.base_corpus_validator import (
    BaseCorpusValidator,
)


class TokenValidator(
    BaseCorpusValidator[Token],
):
    """
    Validator for Token objects.
    """

    def validate(
        self,
        obj: Token,
    ) -> ValidationResult:

        issues: list[ValidationIssue] = []

        if not obj.identifier:
            issues.append(
                ValidationIssue(
                    code="TOK001",
                    message="Token identifier must not be empty.",
                    field="identifier",
                )
            )

        if obj.metadata is None:
            issues.append(
                ValidationIssue(
                    code="TOK002",
                    message="Token metadata is required.",
                    field="metadata",
                )
            )

        if not getattr(obj, "text", "").strip():
            issues.append(
                ValidationIssue(
                    code="TOK003",
                    message="Token text must not be empty.",
                    field="text",
                )
            )

        return ValidationResult.from_issues(issues)
