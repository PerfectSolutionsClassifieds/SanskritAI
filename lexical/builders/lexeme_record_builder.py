
from __future__ import annotations

"""
SanskritAI
==========

Lexeme Record Builder
=====================

Converts a ``LexemeRecord`` into a canonical ``Lexeme``.

Architectural flow
------------------

LexemeRecord
    |
    v
LexemeRecordValidator
    |
    v
LexemeRecordBuilder
    |
    v
LexemeBuilder
    |
    v
Lexeme

The record layer and domain layer deliberately have separate
validation responsibilities.

Version
-------

v0.4.3
"""

from SanskritAI.lexical.builders.base_lexical_record_builder import (
    BaseLexicalRecordBuilder,
)
from SanskritAI.lexical.builders.lexeme_builder import (
    LexemeBuilder,
)
from SanskritAI.lexical.models.lexeme import (
    Lexeme,
)
from SanskritAI.lexical.records.lexeme_record import (
    LexemeRecord,
)
from SanskritAI.lexical.validators.lexeme_record_validator import (
    LexemeRecordValidator,
)


class LexemeRecordBuilder(
    BaseLexicalRecordBuilder[Lexeme],
):
    """
    Convert a validated ``LexemeRecord`` into a ``Lexeme``.
    """

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        """
        Initialize the canonical ValidatedBuilder lifecycle.
        """
        super().__init__(
            validator=LexemeRecordValidator(),
        )

    # ------------------------------------------------------------------
    # Record type
    # ------------------------------------------------------------------

    @property
    def record_type(
        self,
    ) -> type[LexemeRecord]:
        """
        Return the record type consumed by this builder.
        """
        return LexemeRecord

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def build(
        self,
        record: LexemeRecord,
    ) -> Lexeme:
        """
        Convert a valid LexemeRecord into a Lexeme.

        Validation is handled by ``build_validated()`` before this
        method is called.
        """

        if not isinstance(record, LexemeRecord):
            raise TypeError(
                "LexemeRecordBuilder requires a LexemeRecord."
            )

        builder = (
            LexemeBuilder()
            .with_identifier(
                self.normalize_text(record.identifier)
            )
            .with_lemma(
                self.normalize_text(record.lemma)
            )
            .with_normalized(
                self.normalize_optional(record.normalized)
            )
            .with_dictionary(
                record.dictionary
            )
            .with_language(
                record.language
            )
            .with_script(
                record.script
            )
            .with_devanagari(
                self.normalize_optional(record.devanagari)
            )
            .with_iast(
                self.normalize_optional(record.iast)
            )
            .with_transliteration(
                self.normalize_optional(record.transliteration)
            )
            .with_gloss(
                self.normalize_optional(record.gloss)
            )
            .with_notes(
                self.normalize_optional(record.notes)
            )
            .with_tags(
                record.tags
            )
        )

        return builder.build()
