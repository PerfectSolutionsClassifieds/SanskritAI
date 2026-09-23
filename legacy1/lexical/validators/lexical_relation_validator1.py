from __future__ import annotations

"""
SanskritAI
==========

Lexical Relation Validator

Validates LexicalRelation domain objects.

Validation rules
----------------

LEX001
    Lexical relation identifier must not be empty.

LEX002
    Lexical relation source identifier must not be empty.

LEX003
    Lexical relation target identifier must not be empty.

LEX004
    Lexical relation metadata is required.

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
from SanskritAI.lexical.models.lexical_relation import (
    LexicalRelation,
)
from SanskritAI.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class LexicalRelationValidator(
    BaseLexicalValidator[LexicalRelation],
):
    """
    Validator for LexicalRelation objects.

    Validation is intentionally non-short-circuiting. Each
    structural condition is evaluated independently so that
    callers receive all applicable validation issues in one
    result.
    """

    def validate(
        self,
        obj: LexicalRelation,
    ) -> ValidationResult:
        """
        Validate a LexicalRelation and return all applicable
        validation issues.
        """

        issues: list[ValidationIssue] = []

        # -----------------------------------------------------
        # LEX001 — Relation identifier
        # -----------------------------------------------------

        if not obj.identifier:
            issues.append(
                ValidationIssue(
                    code="LEX001",
                    message=(
                        "Lexical relation identifier must not be empty."
                    ),
                    field="identifier",
                )
            )

        # -----------------------------------------------------
        # LEX004 — Metadata
        # -----------------------------------------------------
        #
        # The domain model stores metadata in _metadata.
        # Tests may deliberately set this backing field to None.
        #
        # We therefore inspect the actual backing state rather
        # than relying on a potentially fallback-based public
        # metadata property.
        # -----------------------------------------------------

        metadata = getattr(
            obj,
            "_metadata",
            None,
        )

        if metadata is None:
            issues.append(
                ValidationIssue(
                    code="LEX004",
                    message=(
                        "Lexical relation metadata is required."
                    ),
                    field="metadata",
                )
            )

            # Without metadata there is no source or target
            # identifier to validate.
            return ValidationResult.from_issues(issues)

        # -----------------------------------------------------
        # LEX002 — Source identifier
        # -----------------------------------------------------

        if not metadata.source_identifier:
            issues.append(
                ValidationIssue(
                    code="LEX002",
                    message=(
                        "Lexical relation source identifier "
                        "must not be empty."
                    ),
                    field="source_identifier",
                )
            )

        # -----------------------------------------------------
        # LEX003 — Target identifier
        # -----------------------------------------------------

        if not metadata.target_identifier:
            issues.append(
                ValidationIssue(
                    code="LEX003",
                    message=(
                        "Lexical relation target identifier "
                        "must not be empty."
                    ),
                    field="target_identifier",
                )
            )

        # -----------------------------------------------------
        # Result
        # -----------------------------------------------------

        return ValidationResult.from_issues(issues)


__all__ = [
    "LexicalRelationValidator",
]
