from __future__ import annotations

"""
SanskritAI
==========

Synset Validator

Validates Amarakośa Synset objects.

Version
-------
v0.4.0
"""

from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.validators.base_knowledge_validator import (
    BaseKnowledgeValidator,
)
from SanskritAI.core.validators.validation_issue import (
    ValidationIssue,
)
from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)


class SynsetValidator(
    BaseKnowledgeValidator[Synset],
):
    """
    Validator for Synset objects.
    """

    def validate(
        self,
        obj: Synset,
    ) -> ValidationResult:

        issues: list[ValidationIssue] = []

        if not obj.identifier:
            issues.append(
                ValidationIssue(
                    code="SYN001",
                    message="Synset identifier must not be empty.",
                    field="identifier",
                )
            )

        if obj.metadata is None:
            issues.append(
                ValidationIssue(
                    code="SYN002",
                    message="Synset metadata is required.",
                    field="metadata",
                )
            )

        if len(obj.children) == 0:
            issues.append(
                ValidationIssue(
                    code="SYN003",
                    message="A Synset should contain at least one Lexeme.",
                    field="children",
                )
            )

        return ValidationResult.from_issues(issues)
