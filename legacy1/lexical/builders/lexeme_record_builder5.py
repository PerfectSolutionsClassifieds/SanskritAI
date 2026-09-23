
from __future__ import annotations

"""
SanskritAI
=========

Lexeme Record Builder
=====================

Builds a ``Lexeme`` domain object from a ``LexemeRecord``.

Architectural flow
------------------

LexemeRecord
    ↓
LexemeRecordBuilder
    ↓
LexemeBuilder
    ↓
Lexeme

Validation is performed before domain-object construction through
the canonical ``ValidatedBuilder`` lifecycle.
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
from SanskritAI.lexical.models.lexeme_record import (
    LexemeRecord,
)
from SanskritAI.lexical.validators.lexeme_validator import (
    LexemeValidator,
)


class LexemeRecordBuilder(
    BaseLexicalRecordBuilder[Lexeme],
):
    """
    Convert a ``LexemeRecord`` into a ``Lexeme``.

    The validator belongs to this record-builder and is used by the
    inherited ``build_validated()`` and ``build_many()`` methods.
    """

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        """
        Initialize the canonical ValidatedBuilder lifecycle.
        """
        super().__init__(
            validator=LexemeValidator(),
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
