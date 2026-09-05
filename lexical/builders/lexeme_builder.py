
from __future__ import annotations

"""
SanskritAI
=========

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

The builder conforms to the Architectural Kernel
``NodeBuilder`` / ``BaseBuilder`` lifecycle by maintaining the
current immutable ``Lexeme`` through ``_instance``.

Important
---------

``Lexeme`` itself is not a dataclass.

``LexemeMetadata`` is a frozen dataclass.

Therefore:

* ``dataclasses.replace()`` is used only for ``LexemeMetadata``.
* A new ``Lexeme`` is explicitly constructed when the identifier changes.
* The inherited ``BaseBuilder`` lifecycle remains authoritative.

Version
-------

v0.4.3
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

    The builder uses the canonical ``BaseBuilder`` ``_instance``
    as its single source of state.

    Because ``Lexeme`` and ``LexemeMetadata`` are immutable,
    fluent operations replace the current immutable instance
    rather than mutating it.
    """

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        """
        Initialize the canonical BaseBuilder lifecycle.

        ``BaseBuilder.__init__()`` invokes ``_create_instance()``,
        which creates the default immutable Lexeme.
        """
        super().__init__()

    # ------------------------------------------------------------------
    # Architectural construction
    # ------------------------------------------------------------------

    def _create_instance(self) -> Lexeme:
        """
        Create the default immutable Lexeme instance.

        This method is invoked by ``BaseBuilder.__init__()`` and
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

        ``LexemeMetadata`` is a frozen dataclass, so
        ``dataclasses.replace()`` is appropriate here.
        """
        metadata = replace(
            self._instance.metadata,
            **changes,
        )

        self._instance = Lexeme(
            identifier=self._instance.identifier,
            metadata=metadata,
        )

        return self

    # ------------------------------------------------------------------
    # Internal Lexeme replacement
    # ------------------------------------------------------------------

    def _replace_lexeme(
        self,
        *,
        identifier: str | None = None,
        metadata: LexemeMetadata | None = None,
    ) -> "LexemeBuilder":
        """
        Construct a new Lexeme from the current immutable state.

        ``Lexeme`` is a regular immutable domain object rather than
        a dataclass, so ``dataclasses.replace()`` must not be used
        against it.
        """
        self._instance = Lexeme(
            identifier=(
                self._instance.identifier
                if identifier is None
                else identifier
            ),
            metadata=(
                self._instance.metadata
                if metadata is None
                else metadata
            ),
        )

        return self

    # ------------------------------------------------------------------
    # Compatibility/source metadata
    # ------------------------------------------------------------------

    def _with_extra(
        self,
        key: str,
        value,
    ) -> "LexemeBuilder":
        """
        Preserve compatibility/source fields in ``metadata.extra``.

        ``extra`` itself is represented as a mutable dictionary inside
        the immutable metadata object, so a copied dictionary is used
        before rebuilding the frozen metadata instance.
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

        ``Lexeme`` is not a dataclass, therefore a new ``Lexeme`` is
        explicitly constructed instead of using ``dataclasses.replace``.
        """
        return self._replace_lexeme(
            identifier=identifier,
        )

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
        metadata title, preserving the established builder behavior.
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
        """Set the transliteration."""
        return self._replace_metadata(
            transliteration=transliteration,
        )

    def with_part_of_speech(
        self,
        part_of_speech,
    ) -> "LexemeBuilder":
        """Set the grammatical category."""
        return self._replace_metadata(
            part_of_speech=part_of_speech,
        )

    def with_root(
        self,
        root: str,
    ) -> "LexemeBuilder":
        """Set the lexical root / Dhātu."""
        return self._replace_metadata(
            root=root,
        )

    def with_frequency(
        self,
        frequency: int,
    ) -> "LexemeBuilder":
        """Set corpus frequency."""
        return self._replace_metadata(
            frequency=frequency,
        )

    def with_language(
        self,
        language,
    ) -> "LexemeBuilder":
        """Set lexical language."""
        return self._replace_metadata(
            language=language,
        )

    def with_script(
        self,
        script,
    ) -> "LexemeBuilder":
        """Set writing script."""
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
        """Preserve Devanagari surface form."""
        return self._with_extra(
            "devanagari",
            devanagari,
        )

    def with_iast(
        self,
        iast: str,
    ) -> "LexemeBuilder":
        """Preserve IAST representation."""
        return self._with_extra(
            "iast",
            iast,
        )

    def with_gloss(
        self,
        gloss: str,
    ) -> "LexemeBuilder":
        """Preserve concise lexical gloss."""
        return self._with_extra(
            "gloss",
            gloss,
        )

    def with_notes(
        self,
        notes: str,
    ) -> "LexemeBuilder":
        """Preserve editorial/source notes."""
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
        Build the current immutable Lexeme.

        The canonical BaseBuilder lifecycle is used for validation
        and defensive copying.
        """
        return super().build()
