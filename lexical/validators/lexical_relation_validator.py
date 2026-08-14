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

Validation is intentionally non-short-circuiting for independent
validation rules.

Metadata handling
-----------------
LexicalRelation inherits from BaseNode, whose canonical metadata
storage is the public ``metadata`` attribute.

The test suite may explicitly assign ``_metadata = None`` to
simulate a missing metadata object. Therefore:

    * normal objects use ``obj.metadata``;
    * an explicitly present ``_metadata is None`` is treated as
      missing metadata and produces LEX004.

When metadata is absent, source/target validation is not attempted.

Whitespace-only identifiers are intentionally accepted.

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
    """

    def validate(
        self,
        obj: LexicalRelation,
    ) -> ValidationResult:
        """
        Validate a LexicalRelation.

        All applicable structural issues are collected and
        returned together.

        The validator does not retain state between calls.
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
        # Metadata resolution
        # -----------------------------------------------------
        #
        # BaseNode stores metadata as ``obj.metadata``.
        #
        # However, the validation contract allows the backing
        # ``_metadata`` attribute to be explicitly assigned None
        # in order to represent a missing metadata object.
        #
        # Therefore we distinguish:
        #
        #   no _metadata attribute
        #       -> normal object -> use obj.metadata
        #
        #   _metadata exists and is None
        #       -> explicitly missing -> LEX004
        #
        #   _metadata exists and is not None
        #       -> use that metadata object
        #
        # This preserves compatibility with both the domain model
        # and the validator's structural test contract.
        # -----------------------------------------------------

        metadata_override = getattr(
            obj,
            "_metadata",
            None,
        )

        has_metadata_override = hasattr(
            obj,
            "_metadata",
        )

        if has_metadata_override:
            metadata = metadata_override
        else:
            metadata = getattr(
                obj,
                "metadata",
                None,
            )

        # -----------------------------------------------------
        # LEX004 — Metadata required
        # -----------------------------------------------------

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

            # Metadata-dependent validation cannot proceed.
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
