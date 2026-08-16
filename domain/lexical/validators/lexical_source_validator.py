from __future__ import annotations

"""
SanskritAI
==========

Lexical Source Validator
------------------------

Validates the structural integrity of a domain-level
LexicalSource.

This validator checks provenance metadata only. It does not
validate the historical authenticity or scholarly correctness
of a dictionary source.
"""

from SanskritAI.core.validators.validation_result import ValidationResult
from SanskritAI.domain.lexical.lexical_source import LexicalSource
from SanskritAI.domain.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class LexicalSourceValidator(
    BaseLexicalValidator[LexicalSource],
):
    """
    Validates immutable LexicalSource instances.
    """

    @classmethod
    def supports(
        cls,
        obj: object,
    ) -> bool:
        return isinstance(obj, LexicalSource)

    def validate(
        self,
        obj: LexicalSource,
    ) -> ValidationResult:
        """
        Validate one LexicalSource.

        All structural issues are collected before returning.
        """

        issues = []

        # -----------------------------------------------------
        # Type
        # -----------------------------------------------------

        if not isinstance(obj, LexicalSource):
            issues.append(
                self.error(
                    code="LEXSRC000",
                    message="Object must be a LexicalSource instance.",
                    suggestion="Provide a valid LexicalSource object.",
                )
            )

            return self.result_from_issues(*issues)

        # -----------------------------------------------------
        # Source identifier
        # -----------------------------------------------------

        if self.is_blank(obj.source_id):
            issues.append(
                self.error(
                    code="LEXSRC001",
                    message="Lexical source identifier must not be empty.",
                    field="source_id",
                    suggestion=(
                        "Provide a non-empty lexical source identifier."
                    ),
                )
            )

        # -----------------------------------------------------
        # Source name
        # -----------------------------------------------------

        if self.is_blank(obj.name):
            issues.append(
                self.error(
                    code="LEXSRC002",
                    message="Lexical source name must not be empty.",
                    field="name",
                    suggestion=(
                        "Provide a human-readable source name."
                    ),
                )
            )

        # -----------------------------------------------------
        # Source type
        # -----------------------------------------------------

        if obj.source_type is None:
            issues.append(
                self.error(
                    code="LEXSRC003",
                    message="Lexical source type must be provided.",
                    field="source_type",
                    suggestion=(
                        "Provide a valid DictionarySource value."
                    ),
                )
            )

        # -----------------------------------------------------
        # Language
        # -----------------------------------------------------

        if self.is_blank(obj.language):
            issues.append(
                self.error(
                    code="LEXSRC004",
                    message="Lexical source language must not be empty.",
                    field="language",
                    suggestion=(
                        "Provide the language associated with the source."
                    ),
                )
            )

        # -----------------------------------------------------
        # Script
        # -----------------------------------------------------

        if self.is_blank(obj.script):
            issues.append(
                self.error(
                    code="LEXSRC005",
                    message="Lexical source script must not be empty.",
                    field="script",
                    suggestion=(
                        "Provide the primary script of the source."
                    ),
                )
            )

        # -----------------------------------------------------
        # URL
        # -----------------------------------------------------

        if obj.url and not (
            obj.url.startswith("http://")
            or obj.url.startswith("https://")
        ):
            issues.append(
                self.warning(
                    code="LEXSRC006",
                    message=(
                        "Lexical source URL does not use an HTTP or "
                        "HTTPS scheme."
                    ),
                    field="url",
                    suggestion=(
                        "Use a complete HTTP or HTTPS URL when available."
                    ),
                )
            )

        return self.result_from_issues(*issues)
