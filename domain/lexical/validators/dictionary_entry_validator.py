
from __future__ import annotations

"""
SanskritAI
==========

Dictionary Entry Validator
---------------------------

Structural validation for the canonical lexical DictionaryEntry.

The validator verifies structural integrity only. It does not attempt
to determine whether the lexical or linguistic content is correct.
"""

from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.domain.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)
from SanskritAI.lexical.models.dictionary_entry import (
    DictionaryEntry,
)


class DictionaryEntryValidator(
    BaseLexicalValidator[DictionaryEntry],
):
    """
    Validate canonical DictionaryEntry instances.
    """

    @classmethod
    def supports(
        cls,
        obj: object,
    ) -> bool:
        return isinstance(obj, DictionaryEntry)

    def validate(
        self,
        obj: DictionaryEntry,
    ) -> ValidationResult:

        issues = []

        # -----------------------------------------------------
        # Type
        # -----------------------------------------------------

        if not isinstance(obj, DictionaryEntry):
            issues.append(
                self.error(
                    code="DIC001",
                    message=(
                        "Object must be a canonical "
                        "DictionaryEntry instance."
                    ),
                    suggestion=(
                        "Provide a valid lexical DictionaryEntry object."
                    ),
                )
            )

            return self.result_from_issues(*issues)

        metadata = obj.metadata

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
        # Headword
        # -----------------------------------------------------

        if self.is_blank(metadata.headword):
            issues.append(
                self.text_error(
                    code="DIC003",
                    field="metadata.headword",
                    label="Dictionary entry headword",
                )
            )

        # -----------------------------------------------------
        # Lemma
        # -----------------------------------------------------

        if self.is_blank(metadata.lemma):
            issues.append(
                self.text_error(
                    code="DIC004",
                    field="metadata.lemma",
                    label="Dictionary entry lemma",
                )
            )

        # -----------------------------------------------------
        # Language
        # -----------------------------------------------------

        if self.is_blank(metadata.language):
            issues.append(
                self.text_error(
                    code="DIC005",
                    field="metadata.language",
                    label="Dictionary entry language",
                )
            )

        # -----------------------------------------------------
        # Dictionary
        # -----------------------------------------------------

        if self.is_blank(metadata.dictionary_name):
            issues.append(
                self.warning(
                    code="DIC006",
                    field="metadata.dictionary_name",
                    message=(
                        "Dictionary entry dictionary_name is empty."
                    ),
                    suggestion=(
                        "Provide the dictionary or lexical source name "
                        "when available."
                    ),
                )
            )

        # -----------------------------------------------------
        # Source
        # -----------------------------------------------------

        if obj.source is None:
            issues.append(
                self.warning(
                    code="DIC007",
                    field="source",
                    message="Dictionary entry source is empty.",
                    suggestion=(
                        "Provide the canonical LexicalSource "
                        "when source information is available."
                    ),
                )
            )

        # -----------------------------------------------------
        # Transliteration
        # -----------------------------------------------------

        if not isinstance(metadata.transliteration, str):
            issues.append(
                self.error(
                    code="DIC008",
                    field="metadata.transliteration",
                    message=(
                        "Dictionary entry transliteration "
                        "must be a string."
                    ),
                    suggestion="Provide transliteration as text.",
                )
            )

        # -----------------------------------------------------
        # Entry identifier
        # -----------------------------------------------------

        if not isinstance(metadata.entry_identifier, str):
            issues.append(
                self.error(
                    code="DIC009",
                    field="metadata.entry_identifier",
                    message=(
                        "Dictionary entry entry_identifier "
                        "must be a string."
                    ),
                    suggestion=(
                        "Provide the dictionary-specific identifier "
                        "as text."
                    ),
                )
            )

        return self.result_from_issues(*issues)
