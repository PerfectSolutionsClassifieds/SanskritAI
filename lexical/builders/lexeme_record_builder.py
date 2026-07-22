from __future__ import annotations

"""
SanskritAI
==========

Lexeme Record Builder

Concrete adapter that transforms immutable LexemeRecord
instances into Lexeme domain objects.

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
v0.4.0
"""

from SanskritAI.core.typing import TIdentifier
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
from SanskritAI.lexical.validators.lexeme_validator import (
    LexemeValidator,
)


class LexemeRecordBuilder(
    BaseLexicalRecordBuilder[Lexeme],
):
    """
    Adapter that converts a LexemeRecord into a Lexeme.
    """

    def __init__(self) -> None:
        super().__init__(
            validator=LexemeValidator(),
        )

    @property
    def record_type(self) -> type[LexemeRecord]:
        return LexemeRecord

    def build(
        self,
        record: LexemeRecord,
    ) -> Lexeme:
        """
        Convert a validated LexemeRecord into a Lexeme.
        """

        builder = LexemeBuilder()

        builder \
            .with_identifier(record.identifier) \
            .with_lemma(
                self.normalize_text(record.lemma)
            ) \
            .with_normalized(
                self.normalize_optional(
                    record.normalized
                )
            ) \
            .with_language(record.language) \
            .with_script(record.script) \
            .with_dictionary(record.dictionary) \
            .with_devanagari(
                record.devanagari
            ) \
            .with_iast(
                record.iast
            ) \
            .with_transliteration(
                record.transliteration
            ) \
            .with_gloss(
                record.gloss
            ) \
            .with_notes(
                record.notes
            ) \
            .with_tags(
                list(record.tags)
            )

        return builder.build()
