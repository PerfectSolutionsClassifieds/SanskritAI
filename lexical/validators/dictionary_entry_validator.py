from __future__ import annotations

"""
SanskritAI
==========

Dictionary Entry Validator

Validates DictionaryEntry domain objects.

Validation rules
----------------

LEX001
    Dictionary entry identifier must not be empty.

LEX002
    Dictionary entry source is required.

LEX003
    Dictionary entry metadata is required.

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
from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)
from SanskritAI.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class DictionaryEntryValidator(
    BaseLexicalValidator[DictionaryEntry],
):
    """
    Validator for DictionaryEntry objects.
    """

    def validate(
        self,
        obj: DictionaryEntry,
    ) -> ValidationResult:
        """
        Validate a DictionaryEntry and return all applicable
        validation issues.

        Validation is intentionally non-short-circuiting so that
        identifier, source, and metadata problems can be reported
        together.
        """

        issues: list[ValidationIssue] = []

        # -----------------------------------------------------
        # LEX001 — Identifier
        # -----------------------------------------------------

        if not obj.identifier:
            issues.append(
                ValidationIssue(
                    code="LEX001",
                    message="Dictionary entry identifier must not be empty.",
                    field="identifier",
                )
            )

        # -----------------------------------------------------
        # LEX002 — Source
        # -----------------------------------------------------

        if obj.source is None:
            issues.append(
                ValidationIssue(
                    code="LEX002",
                    message="Dictionary entry source is required.",
                    field="source",
                )
            )

        # -----------------------------------------------------
        # LEX003 — Metadata
        # -----------------------------------------------------

        if hasattr(obj, "_metadata"):
            metadata = getattr(obj, "_metadata")
        else:
            metadata = getattr(obj, "metadata", None)

        if metadata is None:
            issues.append(
                ValidationIssue(
                    code="LEX003",
                    message="Dictionary entry metadata is required.",
                    field="metadata",
                )
            )

        # -----------------------------------------------------
        # Result
        # -----------------------------------------------------

        return ValidationResult.from_issues(issues)
