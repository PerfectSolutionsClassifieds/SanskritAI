
from __future__ import annotations

"""
SanskritAI
==========

Synset Record Builder

Concrete adapter converting immutable SynsetRecord objects
into Synset domain objects.

Pipeline
--------

SynsetRecord
      ↓
SynsetValidator
      ↓
SynsetRecordBuilder
      ↓
SynsetBuilder
      ↓
Synset

Lexeme resolution boundary
--------------------------

SynsetRecord.lexeme_ids
      ↓
Amarakośa orchestration
      ↓
LexicalRepository.get_lexeme(...)
      ↓
canonical Lexeme objects
      ↓
SynsetRecordBuilder.with_lexemes(...)
      ↓
SynsetBuilder.add_lexeme(...)

Version
-------

v0.5.0
"""

from collections.abc import Iterable

from SanskritAI.amarakosha.builders.base_knowledge_record_builder import (
    BaseKnowledgeRecordBuilder,
)
from SanskritAI.amarakosha.builders.synset_builder import (
    SynsetBuilder,
)
from SanskritAI.amarakosha.models.synset import Synset
from SanskritAI.amarakosha.records.synset_record import SynsetRecord
from SanskritAI.amarakosha.validators.synset_validator import (
    SynsetValidator,
)
from SanskritAI.core.records.knowledge_record import (
    KnowledgeRecord,
)
from SanskritAI.lexical.models.lexeme import Lexeme


class SynsetRecordBuilder(
    BaseKnowledgeRecordBuilder[Synset],
):
    """
    Adapter converting knowledge records into Synset objects.

    The builder is intentionally independent of LexicalRepository.

    Lexeme identifiers contained in a SynsetRecord are resolved by
    the Amarakośa orchestration layer. The resulting canonical Lexeme
    objects are then supplied to this builder.
    """

    def __init__(self) -> None:
        super().__init__(
            validator=SynsetValidator(),
        )

        self._resolved_lexemes: tuple[Lexeme, ...] = ()

    # ------------------------------------------------------------------
    # Record contract
    # ------------------------------------------------------------------

    @property
    def record_type(self) -> type[KnowledgeRecord]:
        return KnowledgeRecord

    # ------------------------------------------------------------------
    # Resolved Lexeme boundary
    # ------------------------------------------------------------------

    def with_lexemes(
        self,
        lexemes: Iterable[Lexeme],
    ) -> "SynsetRecordBuilder":
        """
        Supply canonical Lexeme objects resolved by orchestration.

        Repository lookup deliberately does not occur inside this
        builder.
        """

        resolved = tuple(lexemes)

        for lexeme in resolved:
            if not isinstance(lexeme, Lexeme):
                raise TypeError(
                    "SynsetRecordBuilder requires canonical "
                    "SanskritAI.lexical.models.lexeme.Lexeme objects."
                )

        self._resolved_lexemes = resolved

        return self

    def clear_lexemes(self) -> "SynsetRecordBuilder":
        """
        Clear previously supplied resolved Lexeme objects.
        """

        self._resolved_lexemes = ()

        return self

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(
        self,
        record: KnowledgeRecord,
    ) -> Synset:
        """
        Convert a validated knowledge record into a Synset.

        The record identifier becomes the Synset identifier.

        Resolved canonical Lexeme objects supplied through
        ``with_lexemes()`` become Synset children.
        """

        if not isinstance(record, KnowledgeRecord):
            raise TypeError(
                "SynsetRecordBuilder requires a KnowledgeRecord."
            )

        builder = (
            SynsetBuilder()
            .with_identifier(
                self.normalize_text(record.identifier)
            )
        )

        for lexeme in self._resolved_lexemes:
            builder.add_lexeme(lexeme)

        return builder.build()
