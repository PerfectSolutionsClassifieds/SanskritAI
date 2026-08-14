from __future__ import annotations

"""
SanskritAI
==========

Dictionary Sense Validator

Validates DictionarySense domain objects.

Validation rules
----------------

LEX001
    Dictionary sense identifier must not be empty.

LEX002
    Dictionary sense metadata is required.

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
from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)
from SanskritAI.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class DictionarySenseValidator(
    BaseLexicalValidator[DictionarySense],
):
    """
    Validator for DictionarySense objects.
    """

    def validate(
        self,
        obj: DictionarySense,
    ) -> ValidationResult:
        """
        Validate a DictionarySense and return all applicable
        validation issues.

        Validation is intentionally non-short-circuiting:
        identifier and metadata are validated independently so
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
                    message="Dictionary sense identifier must not be empty.",
                    field="identifier",
                )
            )

        # -----------------------------------------------------
        # LEX002 — Metadata
        # -----------------------------------------------------

        if obj.metadata is None:
            issues.append(
                ValidationIssue(
                    code="LEX002",
                    message="Dictionary sense metadata is required.",
                    field="metadata",
                )
            )

        # -----------------------------------------------------
        # Result
        # -----------------------------------------------------

        return ValidationResult.from_issues(issues)


__all__ = [
    "DictionarySenseValidator",
]
