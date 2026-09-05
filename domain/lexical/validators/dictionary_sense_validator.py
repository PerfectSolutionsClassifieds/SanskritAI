
from __future__ import annotations

"""
SanskritAI
==========

Dictionary Sense Validator
---------------------------

Structural validation for the canonical lexical DictionarySense.

The validator verifies structural integrity only. It does not attempt
to determine whether the semantic definition is lexicographically
correct.
"""

from SanskritAI.core.validators.validation_result import (
    ValidationResult,
)
from SanskritAI.domain.lexical.validators.base_lexical_validator import (
    BaseLexicalValidator,
)
from SanskritAI.lexical.models.dictionary_sense import (
    DictionarySense,
)


class DictionarySenseValidator(
    BaseLexicalValidator[DictionarySense],
):
    """
    Validate canonical DictionarySense instances.
    """

    @classmethod
    def supports(
        cls,
        obj: object,
    ) -> bool:
        return isinstance(obj, DictionarySense)

    def validate(
        self,
        obj: DictionarySense,
    ) -> ValidationResult:

        issues = []

        # -----------------------------------------------------
        # Type
        # -----------------------------------------------------

        if not isinstance(obj, DictionarySense):
            issues.append(
                self.error(
                    code="DS001",
                    message=(
                        "Object must be a canonical "
                        "DictionarySense instance."
                    ),
                    suggestion=(
                        "Provide a valid lexical DictionarySense object."
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
                    code="DS002",
                    field="identifier",
                    label="Dictionary sense identifier",
                )
            )

        # -----------------------------------------------------
        # Definition
        # -----------------------------------------------------

        if self.is_blank(metadata.definition):
            issues.append(
                self.text_error(
                    code="DS003",
                    field="metadata.definition",
                    label="Dictionary sense definition",
                )
            )

        # -----------------------------------------------------
        # Language
        # -----------------------------------------------------

        if self.is_blank(metadata.language):
            issues.append(
                self.text_error(
                    code="DS004",
                    field="metadata.language",
                    label="Dictionary sense language",
                )
            )

        # -----------------------------------------------------
        # Sense number
        # -----------------------------------------------------

        if not isinstance(metadata.sense_number, int):
            issues.append(
                self.error(
                    code="DS005",
                    field="metadata.sense_number",
                    message=(
                        "Dictionary sense sense_number "
                        "must be an integer."
                    ),
                    suggestion=(
                        "Provide the ordinal sense number as an integer."
                    ),
                )
            )
        elif metadata.sense_number < 1:
            issues.append(
                self.error(
                    code="DS006",
                    field="metadata.sense_number",
                    message=(
                        "Dictionary sense sense_number "
                        "must be greater than zero."
                    ),
                    suggestion=(
                        "Use a positive ordinal sense number."
                    ),
                )
            )

        # -----------------------------------------------------
        # Optional textual fields
        # -----------------------------------------------------

        text_fields = (
            ("short_definition", metadata.short_definition, "DS007"),
            ("gloss", metadata.gloss, "DS008"),
            ("semantic_domain", metadata.semantic_domain, "DS009"),
            ("usage_label", metadata.usage_label, "DS010"),
            ("register", metadata.register, "DS011"),
            ("grammatical_note", metadata.grammatical_note, "DS012"),
            ("etymology", metadata.etymology, "DS013"),
            ("notes", metadata.notes, "DS014"),
        )

        for field_name, value, code in text_fields:
            if not isinstance(value, str):
                issues.append(
                    self.error(
                        code=code,
                        field=f"metadata.{field_name}",
                        message=(
                            f"Dictionary sense {field_name} "
                            "must be a string."
                        ),
                        suggestion="Provide the field as text.",
                    )
                )

        # -----------------------------------------------------
        # Supporting collections
        # -----------------------------------------------------

        collections = (
            ("examples", metadata.examples, "DS015"),
            ("citations", metadata.citations, "DS016"),
            ("cross_references", metadata.cross_references, "DS017"),
        )

        for field_name, values, code in collections:

            if not isinstance(values, list):
                issues.append(
                    self.error(
                        code=code,
                        field=f"metadata.{field_name}",
                        message=(
                            f"Dictionary sense {field_name} "
                            "must be a list."
                        ),
                        suggestion=(
                            "Store the collection as a list of strings."
                        ),
                    )
                )
                continue

            for value in values:
                if not isinstance(value, str):
                    issues.append(
                        self.error(
                            code=code,
                            field=f"metadata.{field_name}",
                            message=(
                                f"Every dictionary sense "
                                f"{field_name} value must be a string."
                            ),
                            suggestion=(
                                "Use strings for supporting material."
                            ),
                        )
                    )
                    break

        return self.result_from_issues(*issues)
