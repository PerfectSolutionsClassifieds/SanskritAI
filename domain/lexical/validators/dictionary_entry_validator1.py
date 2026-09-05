
from __future__ import annotations

"""
SanskritAI
==========

Dictionary Entry Validator
---------------------------

Structural validation for DictionaryEntry.

This validator intentionally does not attempt to determine whether
a Sanskrit lexical entry is linguistically correct. Linguistic
validation belongs to higher lexical-analysis layers.
"""

from SanskritAI.core.validators.validation_result import ValidationResult
from SanskritAI.domain.lexical.dictionary_entry import DictionaryEntry
from SanskritAI.domain.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)


class DictionaryEntryValidator(
    BaseLexicalValidator[DictionaryEntry],
):
    """
    Validate DictionaryEntry instances.
    """

    @classmethod
    def supports(
        cls,
        obj: object,
    ) -> bool:
        """
        Return True when the object is a DictionaryEntry.
        """
        return isinstance(obj, DictionaryEntry)

    def validate(
        self,
        obj: DictionaryEntry,
    ) -> ValidationResult:
        """
        Validate one DictionaryEntry.
        """

        issues = []

        # -----------------------------------------------------
        # Type
        # -----------------------------------------------------

        if not isinstance(obj, DictionaryEntry):
            issues.append(
                self.error(
                    code="DIC001",
                    message="Object must be a DictionaryEntry instance.",
                    suggestion="Provide a valid DictionaryEntry object.",
                )
            )

            return self.result_from_issues(*issues)

        # -----------------------------------------------------
        # Identifier
        # -----------------------------------------------------

        if self.is_blank(obj.identifier):
            issues.append(
                self.text_error(
                    code="DIC002",
                    field="identifier",
                    label="Dictionary entry identifier",
                )
            )

        # -----------------------------------------------------
        # Lemma
        # -----------------------------------------------------

        if self.is_blank(obj.lemma):
            issues.append(
                self.text_error(
                    code="DIC003",
                    field="lemma",
                    label="Dictionary entry lemma",
                )
            )

        # -----------------------------------------------------
        # Language
        # -----------------------------------------------------

        if self.is_blank(obj.language):
            issues.append(
                self.text_error(
                    code="DIC004",
                    field="language",
                    label="Dictionary entry language",
                )
            )

        # -----------------------------------------------------
        # Source
        # -----------------------------------------------------

        if self.is_blank(obj.source):
            issues.append(
                self.warning(
                    code="DIC005",
                    message="Dictionary entry source is empty.",
                    field="source",
                    suggestion=(
                        "Provide the dictionary or lexical source "
                        "when source information is available."
                    ),
                )
            )

        # -----------------------------------------------------
        # Transliteration
        # -----------------------------------------------------

        if not isinstance(obj.transliteration, str):
            issues.append(
                self.error(
                    code="DIC006",
                    message="Dictionary entry transliteration must be a string.",
                    field="transliteration",
                    suggestion="Provide transliteration as text.",
                )
            )

        # -----------------------------------------------------
        # Description
        # -----------------------------------------------------

        if not isinstance(obj.description, str):
            issues.append(
                self.error(
                    code="DIC007",
                    message="Dictionary entry description must be a string.",
                    field="description",
                    suggestion="Provide description as text.",
                )
            )

        # -----------------------------------------------------
        # Sense identifiers
        # -----------------------------------------------------

        if not isinstance(obj.senses, tuple):
            issues.append(
                self.error(
                    code="DIC008",
                    message="Dictionary entry senses must be a tuple.",
                    field="senses",
                    suggestion=(
                        "Store sense identifiers as an immutable tuple."
                    ),
                )
            )
        else:
            for sense_identifier in obj.senses:
                if not isinstance(sense_identifier, str):
                    issues.append(
                        self.error(
                            code="DIC009",
                            message=(
                                "Every dictionary sense identifier "
                                "must be a string."
                            ),
                            field="senses",
                            suggestion=(
                                "Use string identifiers for dictionary senses."
                            ),
                        )
                    )
                    break

                if not sense_identifier.strip():
                    issues.append(
                        self.error(
                            code="DIC010",
                            message=(
                                "Dictionary sense identifiers "
                                "must not be empty."
                            ),
                            field="senses",
                            suggestion=(
                                "Remove empty sense identifiers."
                            ),
                        )
                    )
                    break

        return self.result_from_issues(*issues)
