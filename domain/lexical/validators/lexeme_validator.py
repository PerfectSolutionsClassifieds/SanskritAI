
from __future__ import annotations

"""
SanskritAI
==========

Lexeme Validator
----------------

Validates the structural integrity of the current SanskritAI
domain.lexical.Lexeme model.

Validation scope
----------------

This validator checks the structural contract of Lexeme:

    identifier
    lemma
    language
    script
    transliteration
    aliases

It does NOT attempt to determine whether a Sanskrit lemma is
linguistically correct. Linguistic correctness belongs to later
lexical/linguistic knowledge layers.
"""

from SanskritAI.core.validators.validation_result import ValidationResult
from SanskritAI.domain.lexical.lexeme import Lexeme

from SanskritAI.domain.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class LexemeValidator(
    BaseLexicalValidator[Lexeme],
):
    """
    Validates immutable Lexeme instances.
    """

    # =========================================================
    # Capability
    # =========================================================

    @classmethod
    def supports(
        cls,
        obj: object,
    ) -> bool:
        """
        Return True only for Lexeme instances.
        """
        return isinstance(obj, Lexeme)

    # =========================================================
    # Validation
    # =========================================================

    def validate(
        self,
        obj: Lexeme,
    ) -> ValidationResult:
        """
        Validate a single Lexeme.

        The validator reports all structural issues found rather
        than stopping at the first failure.
        """

        issues = []

        # -----------------------------------------------------
        # Type
        # -----------------------------------------------------

        if not isinstance(obj, Lexeme):
            issues.append(
                self.error(
                    code="LEX000",
                    message="Object must be a Lexeme instance.",
                    field="",
                    suggestion="Provide a valid Lexeme object.",
                )
            )
            return self.result_from_issues(*issues)

        # -----------------------------------------------------
        # Identifier
        # -----------------------------------------------------

        if self.is_blank(obj.identifier):
            issues.append(
                self.error(
                    code="LEX001",
                    message="Lexeme identifier must not be empty.",
                    field="identifier",
                    suggestion="Provide a non-empty lexeme identifier.",
                )
            )

        # -----------------------------------------------------
        # Lemma
        # -----------------------------------------------------

        if self.is_blank(obj.lemma):
            issues.append(
                self.error(
                    code="LEX002",
                    message="Lexeme lemma must not be empty.",
                    field="lemma",
                    suggestion="Provide a non-empty canonical lemma.",
                )
            )

        # -----------------------------------------------------
        # Language
        # -----------------------------------------------------

        if self.is_blank(obj.language):
            issues.append(
                self.error(
                    code="LEX003",
                    message="Lexeme language must not be empty.",
                    field="language",
                    suggestion="Provide the language of the lexeme.",
                )
            )

        # -----------------------------------------------------
        # Script
        # -----------------------------------------------------

        if self.is_blank(obj.script):
            issues.append(
                self.error(
                    code="LEX004",
                    message="Lexeme script must not be empty.",
                    field="script",
                    suggestion="Provide the script of the lexeme.",
                )
            )

        # -----------------------------------------------------
        # Transliteration
        # -----------------------------------------------------

        # Transliteration is optional. If supplied, it must be a
        # textual value and must not consist only of whitespace.
        if obj.transliteration is not None:
            if not isinstance(obj.transliteration, str):
                issues.append(
                    self.error(
                        code="LEX005",
                        message="Lexeme transliteration must be a string.",
                        field="transliteration",
                        suggestion="Provide transliteration as text.",
                    )
                )
            elif obj.transliteration.strip() == "":
                issues.append(
                    self.warning(
                        code="LEX006",
                        message=(
                            "Lexeme transliteration is empty and will "
                            "be treated as absent."
                        ),
                        field="transliteration",
                    )
                )

        # -----------------------------------------------------
        # Description
        # -----------------------------------------------------

        if obj.description is not None:
            if not isinstance(obj.description, str):
                issues.append(
                    self.error(
                        code="LEX007",
                        message="Lexeme description must be a string.",
                        field="description",
                        suggestion="Provide description as text.",
                    )
                )

        # -----------------------------------------------------
        # Aliases
        # -----------------------------------------------------

        if not isinstance(obj.aliases, frozenset):
            issues.append(
                self.error(
                    code="LEX008",
                    message="Lexeme aliases must be a frozenset.",
                    field="aliases",
                    suggestion="Provide aliases as a frozenset of strings.",
                )
            )
        else:
            for alias in obj.aliases:
                if not isinstance(alias, str):
                    issues.append(
                        self.error(
                            code="LEX009",
                            message="Every Lexeme alias must be a string.",
                            field="aliases",
                            suggestion="Remove non-string alias values.",
                        )
                    )
                    break

                if not alias.strip():
                    issues.append(
                        self.error(
                            code="LEX010",
                            message="Lexeme aliases must not be empty.",
                            field="aliases",
                            suggestion="Remove empty or whitespace-only aliases.",
                        )
                    )
                    break

        return self.result_from_issues(*issues)
