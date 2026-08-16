from __future__ import annotations

"""
SanskritAI
==========

Lexical Relation Validator
--------------------------

Validates the structural integrity of a domain-level
LexicalRelation.

The validator checks structure only. It does not attempt to
determine whether a relation is linguistically or semantically
correct.
"""
from SanskritAI.models.enums.relation_type import RelationType
from SanskritAI.core.validators.validation_result import ValidationResult
from SanskritAI.domain.lexical.lexical_relation import LexicalRelation
from SanskritAI.domain.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class LexicalRelationValidator(
    BaseLexicalValidator[LexicalRelation],
):
    """
    Validates immutable LexicalRelation instances.
    """

    @classmethod
    def supports(
        cls,
        obj: object,
    ) -> bool:
        return isinstance(obj, LexicalRelation)

    def validate(
        self,
        obj: LexicalRelation,
    ) -> ValidationResult:
        """
        Validate one LexicalRelation.

        All structural issues are collected before returning.
        """

        issues = []

        # -----------------------------------------------------
        # Type
        # -----------------------------------------------------

        # if not isinstance(obj, LexicalRelation):
        #     issues.append(
        #         self.error(
        #             code="LEXREL000",
        #             message="Object must be a LexicalRelation instance.",
        #             suggestion="Provide a valid LexicalRelation object.",
        #         )
        #     )
        if not isinstance(obj.relation_type, RelationType):
            issues.append(
                self.error(
                    code="LEXREL003",
                    message="Relation type must be a valid RelationType.",
                    field="relation_type",
                    suggestion="Provide a valid RelationType value.",
                )
            )
            return self.result_from_issues(*issues)

        # -----------------------------------------------------
        # Relation identifier
        # -----------------------------------------------------

        if self.is_blank(obj.relation_id):
            issues.append(
                self.error(
                    code="LEXREL001",
                    message="Lexical relation identifier must not be empty.",
                    field="relation_id",
                    suggestion=(
                        "Provide a non-empty lexical relation identifier."
                    ),
                )
            )

        # -----------------------------------------------------
        # Source lexeme
        # -----------------------------------------------------

        if self.is_blank(obj.source_lexeme_id):
            issues.append(
                self.error(
                    code="LEXREL002",
                    message="Source lexeme identifier must not be empty.",
                    field="source_lexeme_id",
                    suggestion=(
                        "Provide the identifier of the source lexeme."
                    ),
                )
            )

        # -----------------------------------------------------
        # Relation type
        # -----------------------------------------------------

        if not isinstance(obj.relation_type, object):
            issues.append(
                self.error(
                    code="LEXREL003",
                    message="Relation type must be provided.",
                    field="relation_type",
                    suggestion="Provide a valid RelationType.",
                )
            )

        # -----------------------------------------------------
        # Target lexeme
        # -----------------------------------------------------

        if self.is_blank(obj.target_lexeme_id):
            issues.append(
                self.error(
                    code="LEXREL004",
                    message="Target lexeme identifier must not be empty.",
                    field="target_lexeme_id",
                    suggestion=(
                        "Provide the identifier of the target lexeme."
                    ),
                )
            )

        # -----------------------------------------------------
        # Self relation
        # -----------------------------------------------------

        if (
            not self.is_blank(obj.source_lexeme_id)
            and not self.is_blank(obj.target_lexeme_id)
            and obj.source_lexeme_id == obj.target_lexeme_id
        ):
            issues.append(
                self.warning(
                    code="LEXREL005",
                    message=(
                        "Source and target lexeme identifiers are identical."
                    ),
                    field="target_lexeme_id",
                    suggestion=(
                        "Verify that a self-relation is intentional."
                    ),
                )
            )

        return self.result_from_issues(*issues)
