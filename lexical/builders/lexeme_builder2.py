from __future__ import annotations

"""
SanskritAI
==========

Lexeme Builder
==============

Fluent builder for constructing the immutable ``Lexeme`` domain object.

The builder is intentionally responsible only for assembling the fields
supported by the current Lexeme domain model.  Parser-specific fields are
accepted through compatibility setters and preserved in the builder metadata
where the current domain model provides no dedicated field.

Version
-------
v0.4.0
"""

from SanskritAI.lexical.builders.base_lexical_builder import (
    BaseLexicalBuilder,
)
from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexeme_metadata import LexemeMetadata


class LexemeBuilder(BaseLexicalBuilder[Lexeme]):
    """
    Fluent builder for ``Lexeme``.

    The builder follows the existing lexical architecture:

        LexemeRecord
            ↓
        LexemeRecordBuilder
            ↓
        LexemeBuilder
            ↓
        Lexeme

    Only the canonical fields represented by ``LexemeMetadata`` are mapped
    into the resulting Lexeme.  Additional parser fields are retained in
    metadata ``extra`` so that information is not silently lost.
    """

    def __init__(self) -> None:
        self._identifier: str = ""
        self._metadata: LexemeMetadata = LexemeMetadata()

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def with_identifier(self, identifier: str) -> "LexemeBuilder":
        self._identifier = identifier
        return self

    # ------------------------------------------------------------------
    # Core lexical fields
    # ------------------------------------------------------------------

    def with_lemma(self, lemma: str) -> "LexemeBuilder":
        self._metadata = LexemeMetadata(
            lemma=lemma,
            transliteration=self._metadata.transliteration,
            language=self._metadata.language,
            script=self._metadata.script,
            status=self._metadata.status,
            part_of_speech=self._metadata.part_of_speech,
            root=self._metadata.root,
            frequency=self._metadata.frequency,
            description=self._metadata.description,
            aliases=self._metadata.aliases,
            extra=self._metadata.extra,
            title=self._metadata.title or lemma,
        )
        return self

    def with_transliteration(
        self,
        transliteration: str,
    ) -> "LexemeBuilder":
        self._metadata = LexemeMetadata(
            lemma=self._metadata.lemma,
            transliteration=transliteration,
            language=self._metadata.language,
            script=self._metadata.script,
            status=self._metadata.status,
            part_of_speech=self._metadata.part_of_speech,
            root=self._metadata.root,
            frequency=self._metadata.frequency,
            description=self._metadata.description,
            aliases=self._metadata.aliases,
            extra=self._metadata.extra,
            title=self._metadata.title,
        )
        return self

    def with_part_of_speech(self, part_of_speech) -> "LexemeBuilder":
        self._metadata = LexemeMetadata(
            lemma=self._metadata.lemma,
            transliteration=self._metadata.transliteration,
            language=self._metadata.language,
            script=self._metadata.script,
            status=self._metadata.status,
            part_of_speech=part_of_speech,
            root=self._metadata.root,
            frequency=self._metadata.frequency,
            description=self._metadata.description,
            aliases=self._metadata.aliases,
            extra=self._metadata.extra,
            title=self._metadata.title,
        )
        return self

    def with_root(self, root: str) -> "LexemeBuilder":
        self._metadata = LexemeMetadata(
            lemma=self._metadata.lemma,
            transliteration=self._metadata.transliteration,
            language=self._metadata.language,
            script=self._metadata.script,
            status=self._metadata.status,
            part_of_speech=self._metadata.part_of_speech,
            root=root,
            frequency=self._metadata.frequency,
            description=self._metadata.description,
            aliases=self._metadata.aliases,
            extra=self._metadata.extra,
            title=self._metadata.title,
        )
        return self

    def with_frequency(self, frequency: int) -> "LexemeBuilder":
        self._metadata = LexemeMetadata(
            lemma=self._metadata.lemma,
            transliteration=self._metadata.transliteration,
            language=self._metadata.language,
            script=self._metadata.script,
            status=self._metadata.status,
            part_of_speech=self._metadata.part_of_speech,
            root=self._metadata.root,
            frequency=frequency,
            description=self._metadata.description,
            aliases=self._metadata.aliases,
            extra=self._metadata.extra,
            title=self._metadata.title,
        )
        return self

    def with_language(self, language) -> "LexemeBuilder":
        self._metadata = LexemeMetadata(
            lemma=self._metadata.lemma,
            transliteration=self._metadata.transliteration,
            language=language,
            script=self._metadata.script,
            status=self._metadata.status,
            part_of_speech=self._metadata.part_of_speech,
            root=self._metadata.root,
            frequency=self._metadata.frequency,
            description=self._metadata.description,
            aliases=self._metadata.aliases,
            extra=self._metadata.extra,
            title=self._metadata.title,
        )
        return self

    def with_script(self, script) -> "LexemeBuilder":
        self._metadata = LexemeMetadata(
            lemma=self._metadata.lemma,
            transliteration=self._metadata.transliteration,
            language=self._metadata.language,
            script=script,
            status=self._metadata.status,
            part_of_speech=self._metadata.part_of_speech,
            root=self._metadata.root,
            frequency=self._metadata.frequency,
            description=self._metadata.description,
            aliases=self._metadata.aliases,
            extra=self._metadata.extra,
            title=self._metadata.title,
        )
        return self

    # ------------------------------------------------------------------
    # Record compatibility fields
    #
    # These fields originate in LexemeRecord.  The current Lexeme model
    # has no dedicated attributes for them, so preserve them in
    # LexemeMetadata.extra instead of silently dropping them.
    # ------------------------------------------------------------------

    def _with_extra(self, key: str, value) -> "LexemeBuilder":
        extra = dict(self._metadata.extra)
        extra[key] = value

        self._metadata = LexemeMetadata(
            lemma=self._metadata.lemma,
            transliteration=self._metadata.transliteration,
            language=self._metadata.language,
            script=self._metadata.script,
            status=self._metadata.status,
            part_of_speech=self._metadata.part_of_speech,
            root=self._metadata.root,
            frequency=self._metadata.frequency,
            description=self._metadata.description,
            aliases=self._metadata.aliases,
            extra=extra,
            title=self._metadata.title,
        )
        return self

    def with_normalized(self, normalized: str) -> "LexemeBuilder":
        return self._with_extra("normalized", normalized)

    def with_dictionary(self, dictionary) -> "LexemeBuilder":
        return self._with_extra("dictionary", dictionary)

    def with_devanagari(self, devanagari: str) -> "LexemeBuilder":
        return self._with_extra("devanagari", devanagari)

    def with_iast(self, iast: str) -> "LexemeBuilder":
        return self._with_extra("iast", iast)

    def with_gloss(self, gloss: str) -> "LexemeBuilder":
        return self._with_extra("gloss", gloss)

    def with_notes(self, notes: str) -> "LexemeBuilder":
        return self._with_extra("notes", notes)

    def with_tags(self, tags) -> "LexemeBuilder":
        return self._with_extra("tags", tuple(tags))

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def build(self) -> Lexeme:
        """
        Construct the immutable Lexeme.

        The existing Lexeme constructor remains the final authority for
        object creation.
        """
        return Lexeme(
            identifier=self._identifier,
            metadata=self._metadata,
        )
