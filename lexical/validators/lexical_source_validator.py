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

LEX003
    Lexical source metadata is required.

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

    The validator checks only the structural invariants owned by
    LexicalSource itself. It does not attempt to validate nested
    metadata fields.
    """

    def validate(
        self,
        obj: LexicalSource,
    ) -> ValidationResult:
        """
        Validate a LexicalSource and return all applicable
        validation issues.

        Validation is intentionally non-short-circuiting so that
        callers receive all structural problems in one result.
        """

        issues: list[ValidationIssue] = []

        # ---------------------------------------------------------
        # LEX001 — Identifier
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # LEX002 — Name
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # LEX003 — Metadata
        # ---------------------------------------------------------
        #
        # LexicalSource exposes metadata through its public
        # interface, but the domain model permits the backing
        # _metadata field to be explicitly set to None.
        #
        # Validate the backing state directly so a missing metadata
        # object cannot be hidden by a property default/fallback.
        # ---------------------------------------------------------

        metadata = getattr(
            obj,
            "_metadata",
            None,
        )

        if metadata is None:
            issues.append(
                ValidationIssue(
                    code="LEX003",
                    message=(
                        "Lexical source metadata is required."
                    ),
                    field="metadata",
                )
            )

        # ---------------------------------------------------------
        # Result
        # ---------------------------------------------------------

        return ValidationResult.from_issues(issues)


__all__ = [
    "LexicalSourceValidator",
]
