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
    LexemeValidator
        ↓
    LexemeRecordBuilder
        ↓
    LexemeBuilder
        ↓
    Lexeme

Version
-------
v0.4.1
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


class LexemeRecordBuilder(BaseLexicalRecordBuilder[Lexeme]):
    """
    Build a Lexeme domain object from a LexemeRecord.

    Normalization is performed at the record-to-domain boundary so that
    parser records remain immutable source representations while the domain
    receives canonical lexical text.
    """

    def __init__(self) -> None:
        self._validator = LexemeValidator()

    # ------------------------------------------------------------------
    # Contract
    # ------------------------------------------------------------------

    @property
    def record_type(self) -> type[LexemeRecord]:
        return LexemeRecord

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, record: LexemeRecord) -> Lexeme:
        """
        Convert a validated LexemeRecord into a Lexeme.

        Raises
        ------
        TypeError
            If the supplied object is not a LexemeRecord.

        ValueError
            If the record fails lexical validation.
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
