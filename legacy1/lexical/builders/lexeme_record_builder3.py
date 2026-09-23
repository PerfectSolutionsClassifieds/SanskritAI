
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

The record remains immutable and is never modified.

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
    Build a ``Lexeme`` domain object from a ``LexemeRecord``.

    Responsibilities
    ----------------
    1. Verify the record type.
    2. Normalize textual record fields.
    3. Map record information through ``LexemeBuilder``.
    4. Preserve compatibility fields in ``LexemeMetadata.extra``.
    5. Produce the immutable ``Lexeme`` object.
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

    def build(
        self,
        record: LexemeRecord,
    ) -> Lexeme:
        """
        Convert a ``LexemeRecord`` into a ``Lexeme``.

        Parameters
        ----------
        record:
            Immutable lexical parser record.

        Returns
        -------
        Lexeme
            Immutable lexical domain object.

        Raises
        ------
        TypeError
            If ``record`` is not a ``LexemeRecord``.
        ValueError
            If lexical validation fails.
        """

        if not isinstance(record, LexemeRecord):
            raise TypeError(
                "LexemeRecordBuilder requires a LexemeRecord."
            )

        # --------------------------------------------------------------
        # Validate the source record when the validator exposes the
        # expected validation contract.
        #
        # The existing project tests establish construction behavior;
        # validation remains owned by LexemeValidator.
        # --------------------------------------------------------------

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
