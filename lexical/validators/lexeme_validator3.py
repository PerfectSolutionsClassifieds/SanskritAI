
from __future__ import annotations

"""
SanskritAI
==========

Lexeme Validator

Validates Lexeme domain objects.

Validation rules
----------------

LEX001
    Lexeme identifier must not be empty.

LEX002
    Lexeme metadata is required.

The validator deliberately reports all applicable issues rather
than stopping at the first failure.

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
        """
        Validate a Lexeme and return all applicable issues.

        Validation is intentionally non-short-circuiting.

        Identifier and metadata are validated independently so
        callers receive the complete set of structural problems
        in a single result.
        """

        issues: list[ValidationIssue] = []

        # -----------------------------------------------------
        # LEX001 — Identifier
        # -----------------------------------------------------

        if not obj.identifier:
            issues.append(
                ValidationIssue(
                    code="LEX001",
                    message="Lexeme identifier must not be empty.",
                    field="identifier",
                )
            )

        # -----------------------------------------------------
        # LEX002 — Metadata
        # -----------------------------------------------------
        #
        # Validate the actual stored metadata object.
        #
        # The Lexeme test suite intentionally exercises the
        # structural failure state by setting:
        #
        #     lexeme._metadata = None
        #
        # Therefore validation must not depend on a higher-level
        # metadata accessor whose behavior may conceal that state.
        # -----------------------------------------------------

        if getattr(obj, "_metadata", None) is None:
            issues.append(
                ValidationIssue(
                    code="LEX002",
                    message="Lexeme metadata is required.",
                    field="metadata",
                )
            )

        # -----------------------------------------------------
        # Result
        # -----------------------------------------------------

        return ValidationResult.from_issues(issues)
