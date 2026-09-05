
from __future__ import annotations

"""
SanskritAI
==========

Lexeme Record Validator
=======================

Validates ``LexemeRecord`` instances before they are converted into
canonical ``Lexeme`` domain objects.

Validation rules
----------------

LEXR001
    Lexeme record identifier must not be empty.

LEXR002
    Lexeme record lemma must not be empty.

The validator is intentionally concerned with the structure of the
record layer. Domain-object validation remains the responsibility of
``LexemeValidator``.

Version
-------

v0.4.3
"""

from SanskritAI.core.validators.validation_issue import (
    ValidationIssue,
)
from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.lexical.records.lexeme_record import (
    LexemeRecord,
)
from SanskritAI.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class LexemeRecordValidator(
    BaseLexicalValidator[LexemeRecord],
):
    """
    Validator for ``LexemeRecord`` objects.

    This validator operates strictly at the record layer and does not
    assume that a LexemeRecord has domain-object metadata.
    """

    def validate(
        self,
        obj: LexemeRecord,
    ) -> ValidationResult:
        """
        Validate a LexemeRecord and return all applicable issues.
        """

        if not isinstance(obj, LexemeRecord):
            return ValidationResult.from_issues(
                [
                    ValidationIssue(
                        code="LEXR000",
                        message="Expected a LexemeRecord.",
                        field="record",
                    )
                ]
            )

        issues: list[ValidationIssue] = []

        # --------------------------------------------------------------
        # LEXR001 — Identifier
        # --------------------------------------------------------------

        if not obj.identifier or not obj.identifier.strip():
            issues.append(
                ValidationIssue(
                    code="LEXR001",
                    message=(
                        "Lexeme record identifier must not be empty."
                    ),
                    field="identifier",
                )
            )

        # --------------------------------------------------------------
        # LEXR002 — Lemma
        # --------------------------------------------------------------

        if not obj.lemma or not obj.lemma.strip():
            issues.append(
                ValidationIssue(
                    code="LEXR002",
                    message=(
                        "Lexeme record lemma must not be empty."
                    ),
                    field="lemma",
                )
            )

        # --------------------------------------------------------------
        # Result
        # --------------------------------------------------------------

        return ValidationResult.from_issues(issues)
