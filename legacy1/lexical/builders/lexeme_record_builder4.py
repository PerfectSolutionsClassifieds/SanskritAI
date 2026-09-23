from __future__ import annotations

"""
SanskritAI
==========

Lexeme Record Builder
=====================

Converts an immutable ``LexemeRecord`` parser record into the current
``Lexeme`` domain object through ``LexemeBuilder``.

Pipeline
--------

LexemeRecord
    ↓
LexemeRecordBuilder
    ↓
LexemeBuilder
    ↓
Lexeme

Validation is orchestrated by ``ValidatedBuilder.build_validated()``.
Direct ``build()`` performs the record-to-domain adaptation.

The source record remains immutable and is never modified.

Version
-------
v0.4.2
"""

from SanskritAI.lexical.builders.base_lexical_record_builder import (
    BaseLexicalRecordBuilder,
)
from SanskritAI.lexical.builders.lexeme_builder import (
    LexemeBuilder,
)
from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.records.lexeme_record import LexemeRecord
from SanskritAI.lexical.validators.lexeme_validator import (
    LexemeValidator,
)


class LexemeRecordBuilder(
    BaseLexicalRecordBuilder[Lexeme],
):
    """
    Build a ``Lexeme`` domain object from a ``LexemeRecord``.
    """

    def __init__(self) -> None:
        super().__init__(
            validator=LexemeValidator(),
        )

    # ------------------------------------------------------------------
    # Contract
    # ------------------------------------------------------------------

    @property
    def record_type(
        self,
    ) -> type[LexemeRecord]:
        """
        Return the supported record type.
        """

        return LexemeRecord

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(
        self,
        record: LexemeRecord,
    ) -> Lexeme:
        """
        Convert a LexemeRecord into a Lexeme.

        Validation is intentionally not performed here.

        Use ``build_validated()`` when validation must be executed
        before construction.
        """

        if not isinstance(record, LexemeRecord):
            raise TypeError(
                "LexemeRecordBuilder requires a LexemeRecord."
            )

        builder = (
            LexemeBuilder()
            .with_identifier(
                self.normalize_text(
                    record.identifier
                )
            )
            .with_lemma(
                self.normalize_text(
                    record.lemma
                )
            )
            .with_normalized(
                self.normalize_optional(
                    record.normalized
                )
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
                self.normalize_optional(
                    record.devanagari
                )
            )
            .with_iast(
                self.normalize_optional(
                    record.iast
                )
            )
            .with_transliteration(
                self.normalize_optional(
                    record.transliteration
                )
            )
            .with_gloss(
                self.normalize_optional(
                    record.gloss
                )
            )
            .with_notes(
                self.normalize_optional(
                    record.notes
                )
            )
            .with_tags(
                record.tags
            )
        )

        return builder.build()
