from __future__ import annotations

"""
SanskritAI
==========

Lexeme Builder
==============

Fluent builder for constructing the immutable ``Lexeme`` domain object.

Architectural flow
------------------

LexemeRecord
    ↓
LexemeRecordBuilder
    ↓
LexemeBuilder
    ↓
Lexeme

The builder conforms to the Architectural Kernel ``NodeBuilder`` /
``BaseBuilder`` lifecycle by maintaining the current immutable
``Lexeme`` through ``_instance``.

Because ``Lexeme`` and ``LexemeMetadata`` are immutable, fluent
operations replace the current instance rather than mutating it.

Version
-------
v0.4.2
"""

from dataclasses import replace

from SanskritAI.lexical.builders.base_lexical_builder import (
    BaseLexicalBuilder,
)
from SanskritAI.lexical.models.lexeme import Lexeme
from SanskritAI.lexical.models.lexeme_metadata import (
    LexemeMetadata,
)


class LexemeBuilder(
    BaseLexicalBuilder[Lexeme],
):
    """
    Fluent builder for ``Lexeme``.

    The builder uses the canonical BaseBuilder ``_instance`` as its
    single source of state.

    Every fluent setter returns ``self`` and replaces the immutable
    current instance with a new instance containing the requested
    change.
    """

    # ------------------------------------------------------------------
    # Architectural construction
    # ------------------------------------------------------------------

    def _create_instance(self) -> Lexeme:
        """
        Create the default immutable Lexeme instance.

        This method is invoked by ``BaseBuilder.__init__()`` and by
        ``BaseBuilder.reset()``.
        """

        return Lexeme(
            identifier="",
            metadata=LexemeMetadata(),
        )

    # ------------------------------------------------------------------
    # Internal metadata replacement
    # ------------------------------------------------------------------

    def _replace_metadata(
        self,
        **changes,
    ) -> "LexemeBuilder":
        """
        Replace selected immutable LexemeMetadata fields.
        """

        metadata = replace(
            self._instance.metadata,
            **changes,
        )

        self._instance = replace(
            self._instance,
            metadata=metadata,
        )

        return self

    def _with_extra(
        self,
        key: str,
        value,
    ) -> "LexemeBuilder":
        """
        Preserve compatibility/source fields in metadata.extra.
        """

        extra = dict(self._instance.metadata.extra)
        extra[key] = value

        return self._replace_metadata(
            extra=extra,
        )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def with_identifier(
        self,
        identifier: str,
    ) -> "LexemeBuilder":
        """
        Set the canonical lexeme identifier.
        """

        self._instance = replace(
            self._instance,
            identifier=identifier,
        )

        return self

    # ------------------------------------------------------------------
    # Core lexical fields
    # ------------------------------------------------------------------

    def with_lemma(
        self,
        lemma: str,
    ) -> "LexemeBuilder":
        """
        Set the canonical lemma.

        If no title has yet been assigned, the lemma becomes the
        metadata title, preserving the previous builder behavior.
        """

        title = (
            self._instance.metadata.title
            or lemma
        )

        return self._replace_metadata(
            lemma=lemma,
            title=title,
        )

    def with_transliteration(
        self,
        transliteration: str,
    ) -> "LexemeBuilder":
        """
        Set the transliteration.
        """

        return self._replace_metadata(
            transliteration=transliteration,
        )

    def with_part_of_speech(
        self,
        part_of_speech,
    ) -> "LexemeBuilder":
        """
        Set the grammatical category.
        """

        return self._replace_metadata(
            part_of_speech=part_of_speech,
        )

    def with_root(
        self,
        root: str,
    ) -> "LexemeBuilder":
        """
        Set the lexical root / Dhātu.
        """

        return self._replace_metadata(
            root=root,
        )

    def with_frequency(
        self,
        frequency: int,
    ) -> "LexemeBuilder":
        """
        Set corpus frequency.
        """

        return self._replace_metadata(
            frequency=frequency,
        )

    def with_language(
        self,
        language,
    ) -> "LexemeBuilder":
        """
        Set lexical language.
        """

        return self._replace_metadata(
            language=language,
        )

    def with_script(
        self,
        script,
    ) -> "LexemeBuilder":
        """
        Set writing script.
        """

        return self._replace_metadata(
            script=script,
        )

    # ------------------------------------------------------------------
    # Record compatibility fields
    # ------------------------------------------------------------------

    def with_normalized(
        self,
        normalized: str,
    ) -> "LexemeBuilder":
        """
        Preserve normalized source information in metadata.extra.
        """

        return self._with_extra(
            "normalized",
            normalized,
        )

    def with_dictionary(
        self,
        dictionary,
    ) -> "LexemeBuilder":
        """
        Preserve dictionary/source classification.
        """

        return self._with_extra(
            "dictionary",
            dictionary,
        )

    def with_devanagari(
        self,
        devanagari: str,
    ) -> "LexemeBuilder":
        """
        Preserve Devanagari surface form.
        """

        return self._with_extra(
            "devanagari",
            devanagari,
        )

    def with_iast(
        self,
        iast: str,
    ) -> "LexemeBuilder":
        """
        Preserve IAST representation.
        """

        return self._with_extra(
            "iast",
            iast,
        )

    def with_gloss(
        self,
        gloss: str,
    ) -> "LexemeBuilder":
        """
        Preserve concise lexical gloss.
        """

        return self._with_extra(
            "gloss",
            gloss,
        )

    def with_notes(
        self,
        notes: str,
    ) -> "LexemeBuilder":
        """
        Preserve editorial/source notes.
        """

        return self._with_extra(
            "notes",
            notes,
        )

    def with_tags(
        self,
        tags,
    ) -> "LexemeBuilder":
        """
        Preserve lexical tags as an immutable tuple.
        """

        return self._with_extra(
            "tags",
            tuple(tags),
        )

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def build(self) -> Lexeme:
        """
        Return the current immutable Lexeme.

        ``BaseBuilder.build()`` performs validation/deep-copy
        semantics at the kernel level. This override preserves the
        existing public LexemeBuilder behavior while returning the
        current immutable instance.
        """

        return self._create_instance_from_current()

    def _create_instance_from_current(self) -> Lexeme:
        """
        Return the current immutable instance.

        Kept separate from ``_create_instance()`` because
        ``_create_instance()`` represents the reset/default state.
        """

        return self._instance
