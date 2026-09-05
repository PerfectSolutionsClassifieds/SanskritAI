from __future__ import annotations

"""
SanskritAI
==========

Lexeme Builder

Fluent builder for constructing Lexeme objects.

Version
-------
v0.3.0
"""

from SanskritAI.lexical.builders.base_lexical_builder import (
    BaseLexicalBuilder,
)
from SanskritAI.lexical.enums.part_of_speech import (
    PartOfSpeech,
)
from SanskritAI.lexical.models.lexeme import (
    Lexeme,
)
from SanskritAI.lexical.models.lexeme_metadata import (
    LexemeMetadata,
)


class LexemeBuilder(
    BaseLexicalBuilder[Lexeme],
):
    """
    Fluent builder for Lexeme objects.
    """

    def __init__(self) -> None:
        super().__init__()

        self._identifier: str = ""
        self._metadata = LexemeMetadata()

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    def with_identifier(
        self,
        identifier: str,
    ) -> "LexemeBuilder":

        self._identifier = identifier
        return self

    # ---------------------------------------------------------
    # Lexical properties
    # ---------------------------------------------------------

    def with_lemma(
        self,
        lemma: str,
    ) -> "LexemeBuilder":

        self._metadata.lemma = lemma
        return self

    # ---------------------------------------------------------

    def with_transliteration(
        self,
        transliteration: str,
    ) -> "LexemeBuilder":

        self._metadata.transliteration = transliteration
        return self

    # ---------------------------------------------------------

    def with_part_of_speech(
        self,
        part_of_speech: PartOfSpeech,
    ) -> "LexemeBuilder":

        self._metadata.part_of_speech = part_of_speech
        return self

    # ---------------------------------------------------------

    def with_root(
        self,
        root: str,
    ) -> "LexemeBuilder":

        self._metadata.root = root
        return self

    # ---------------------------------------------------------

    def with_frequency(
        self,
        frequency: int,
    ) -> "LexemeBuilder":

        self._metadata.frequency = frequency
        return self

    # ---------------------------------------------------------

    def with_language(
        self,
        language: str,
    ) -> "LexemeBuilder":

        self._metadata.language = language
        return self

    # ---------------------------------------------------------

    def with_script(
        self,
        script: str,
    ) -> "LexemeBuilder":

        self._metadata.script = script
        return self

    # ---------------------------------------------------------

    def build(self) -> Lexeme:
        """
        Construct a Lexeme instance.
        """

        return Lexeme(
            identifier=self._identifier,
            metadata=self._metadata,
        )
