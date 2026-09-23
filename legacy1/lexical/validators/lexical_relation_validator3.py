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

The validator deliberately reports all applicable issues rather
than stopping at the first failure.

Important
---------
The validator validates the structural fields represented by the
current LexicalRelation domain contract. It does not validate the
contents of LexicalRelationMetadata beyond the source and target
identifiers.

Whitespace-only strings are intentionally accepted. This is
consistent with the lexical validator contract: only an actually
empty string / falsy identifier is considered missing.

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

    Validation is intentionally non-short-circuiting so that
    callers receive all applicable structural issues in a
    single ValidationResult.
    """

    def validate(
        self,
        obj: LexicalRelation,
    ) -> ValidationResult:
        """
        Validate a LexicalRelation.

        Returns
        -------
        ValidationResult
            A result containing every applicable validation issue.
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
        # Metadata
        # -----------------------------------------------------
        #
        # LexicalRelation provides the metadata object through
        # its public domain interface. The source and target
        # identifiers belong to that metadata.
        #
        # We deliberately do not emit a separate metadata-level
        # error. The current validator contract is concerned with
        # LEX002 and LEX003.
        # -----------------------------------------------------

        metadata = obj.metadata

        # -----------------------------------------------------
        # LEX002 — Source identifier
        # -----------------------------------------------------

        if metadata is not None and not metadata.source_identifier:
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

        if metadata is not None and not metadata.target_identifier:
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
