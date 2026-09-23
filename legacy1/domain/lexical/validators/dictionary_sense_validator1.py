
from __future__ import annotations

"""
SanskritAI
==========

Dictionary Sense Validator
---------------------------

Structural validation for DictionarySense.

This validator verifies the integrity of the dictionary-sense
domain object. It does not attempt to determine whether a
semantic definition is linguistically or lexicographically
correct.
"""

from SanskritAI.core.validators.validation_result import ValidationResult
from SanskritAI.domain.lexical.dictionary_sense import DictionarySense
from SanskritAI.domain.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class DictionarySenseValidator(
    BaseLexicalValidator[DictionarySense],
):
    """
    Validate DictionarySense instances.
    """

    @classmethod
    def supports(
        cls,
        obj: object,
    ) -> bool:
        """
        Return True when the object is a DictionarySense.
        """
        return isinstance(obj, DictionarySense)

    def validate(
        self,
        obj: DictionarySense,
    ) -> ValidationResult:
        """
        Validate one DictionarySense.
        """

        issues = []

        # -----------------------------------------------------
        # Type
        # -----------------------------------------------------

        if not isinstance(obj, DictionarySense):
            issues.append(
                self.error(
                    code="DS001",
                    message="Object must be a DictionarySense instance.",
                    suggestion="Provide a valid DictionarySense object.",
                )
            )

            return self.result_from_issues(*issues)

        # -----------------------------------------------------
        # Identifier
        # -----------------------------------------------------

        if self.is_blank(obj.identifier):
            issues.append(
                self.text_error(
                    code="DS002",
                    field="identifier",
                    label="Dictionary sense identifier",
                )
            )

        # -----------------------------------------------------
        # Entry identifier
        # -----------------------------------------------------

        if self.is_blank(obj.entry_id):
            issues.append(
                self.text_error(
                    code="DS003",
                    field="entry_id",
                    label="Dictionary entry identifier",
                )
            )

        # -----------------------------------------------------
        # Meaning
        # -----------------------------------------------------

        if self.is_blank(obj.meaning):
            issues.append(
                self.text_error(
                    code="DS004",
                    field="meaning",
                    label="Dictionary sense meaning",
                )
            )

        # -----------------------------------------------------
        # Language
        # -----------------------------------------------------

        if self.is_blank(obj.language):
            issues.append(
                self.text_error(
                    code="DS005",
                    field="language",
                    label="Dictionary sense language",
                )
            )

        # -----------------------------------------------------
        # Source
        # -----------------------------------------------------

        if self.is_blank(obj.source):
            issues.append(
                self.warning(
                    code="DS006",
                    field="source",
                    message="Dictionary sense source is empty.",
                    suggestion=(
                        "Provide the dictionary or lexical source "
                        "when source information is available."
                    ),
                )
            )

        # -----------------------------------------------------
        # Optional textual fields
        # -----------------------------------------------------

        if not isinstance(obj.transliteration, str):
            issues.append(
                self.error(
                    code="DS007",
                    field="transliteration",
                    message=(
                        "Dictionary sense transliteration "
                        "must be a string."
                    ),
                    suggestion="Provide transliteration as text.",
                )
            )

        if not isinstance(obj.grammatical_label, str):
            issues.append(
                self.error(
                    code="DS008",
                    field="grammatical_label",
                    message=(
                        "Dictionary sense grammatical_label "
                        "must be a string."
                    ),
                    suggestion="Provide the grammatical label as text.",
                )
            )

        if not isinstance(obj.usage, str):
            issues.append(
                self.error(
                    code="DS009",
                    field="usage",
                    message="Dictionary sense usage must be a string.",
                    suggestion="Provide usage information as text.",
                )
            )

        # -----------------------------------------------------
        # Examples
        # -----------------------------------------------------

        if not isinstance(obj.examples, tuple):
            issues.append(
                self.error(
                    code="DS010",
                    field="examples",
                    message="Dictionary sense examples must be a tuple.",
                    suggestion=(
                        "Store examples as an immutable tuple of strings."
                    ),
                )
            )
        else:
            for example in obj.examples:
                if not isinstance(example, str):
                    issues.append(
                        self.error(
                            code="DS011",
                            field="examples",
                            message=(
                                "Every dictionary sense example "
                                "must be a string."
                            ),
                            suggestion=(
                                "Use strings for dictionary sense examples."
                            ),
                        )
                    )
                    break

                if not example.strip():
                    issues.append(
                        self.error(
                            code="DS012",
                            field="examples",
                            message=(
                                "Dictionary sense examples "
                                "must not be empty."
                            ),
                            suggestion=(
                                "Remove empty example strings."
                            ),
                        )
                    )
                    break

        return self.result_from_issues(*issues)
