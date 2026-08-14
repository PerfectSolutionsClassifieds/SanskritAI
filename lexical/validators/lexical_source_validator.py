
from __future__ import annotations

"""
SanskritAI
==========

Lexical Source Validator

Validates LexicalSource domain objects.

Validation rules
----------------

LEX001
    Lexical source identifier must not be empty.

LEX002
    Lexical source name must not be empty.

Notes
-----

LexicalSource is intentionally a lightweight immutable value object.
It does not expose a metadata object. Therefore this validator does
not perform metadata validation.

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
from SanskritAI.lexical.models.lexical_source import (
    LexicalSource,
)
from SanskritAI.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class LexicalSourceValidator(
    BaseLexicalValidator[LexicalSource],
):
    """
    Validator for LexicalSource objects.
    """

    def validate(
        self,
        obj: LexicalSource,
    ) -> ValidationResult:
        """
        Validate a LexicalSource and return all applicable
        validation issues.

        Validation is intentionally non-short-circuiting:
        identifier and name are validated independently so
        callers receive the complete set of structural problems
        in a single result.

        Whitespace-only values are intentionally accepted.
        The validation rule concerns emptiness, not whitespace
        normalization.
        """

        issues: list[ValidationIssue] = []

        # -----------------------------------------------------
        # LEX001 — Identifier
        # -----------------------------------------------------

        if not obj.identifier:
            issues.append(
                ValidationIssue(
                    code="LEX001",
                    message=(
                        "Lexical source identifier must not be empty."
                    ),
                    field="identifier",
                )
            )

        # -----------------------------------------------------
        # LEX002 — Name
        # -----------------------------------------------------

        if not obj.name:
            issues.append(
                ValidationIssue(
                    code="LEX002",
                    message=(
                        "Lexical source name must not be empty."
                    ),
                    field="name",
                )
            )

        # -----------------------------------------------------
        # Result
        # -----------------------------------------------------

        return ValidationResult.from_issues(issues)


__all__ = [
    "LexicalSourceValidator",
]
